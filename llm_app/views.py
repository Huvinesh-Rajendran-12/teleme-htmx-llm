import os
from random import randint
from uuid import uuid4
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
import requests
from .models import Message
import queue
import json

ENDPOINT = os.getenv('ENDPOINT', '')
MODEL_NAME = os.getenv('MODEL_NAME', '')
STREAM = True if os.getenv('STREAM', 'False').lower() == 'true' else False
MESSAGE_QUEUE = queue.Queue()

# Create your views here.
def index(request):
    session_id = uuid4().hex
    print('session_id', session_id)
    return render(request, "index.html", {'session_id': session_id})

def chat_view(request, session_id):
    if request.method == "POST":
        user_message = request.POST.get('user_input')
        print('user_message', user_message)
        Message.objects.create(session_id=session_id, user_message=user_message)
        MESSAGE_QUEUE.put(user_message)
        return HttpResponse()

def get_existing_messages(session_id) -> list:
    """
    Get all messages from the database and format them for the API.
    """
    formatted_messages = []

    for message in Message.objects.filter(session_id=session_id).values('user_message', 'llm_message'):
        formatted_messages.append({"role": "user", "content": message['user_message']})
        formatted_messages.append({"role": "assistant", "content": message['llm_message']})
    return formatted_messages

def stream(request, session_id):
    def message_stream():
        global new_conversation
        print('session_id', session_id)
        while True:
            # If a message is present in the queue, send it to the clients
            if not MESSAGE_QUEUE.empty():
                message = Message.objects.filter(session_id=session_id).latest('created_at')
                user_message = MESSAGE_QUEUE.get()
                message = Message.objects.filter(session_id=session_id).latest('created_at')
                hx_swap = False
                current_response_id = f"gptblock{randint(67, 999999)}"

                response = ""
            
                for word in chat_response(user_message, session_id):
                    try:
                        response += word.replace("\n", "<br>")

                        ai_message = f"<p>{ response }</p>"

                        # Use flexbox to align "Teleme AI" wording on top of the AI message
                        res = f"""data: <li class="text-white px-4 py-2 m-1 w-1/2 text-md flex flex-col justify-start items-start" id="{current_response_id}" {"hx-swap-oob='true'" if hx_swap else ""}><div><strong>Teleme AI</strong><br>{ai_message}<div></li>\n\n"""

                        hx_swap = True

                        print(f"user: {user_message}")
                        print(res)
                        yield res + "\n\n"  # Add newline characters at the end of each line
                        hx_swap = True
                    except Exception as e:
                        print(e)
                        return e         
                message.current_response_id = current_response_id
                message.llm_message = response
                message.save()
    return StreamingHttpResponse(message_stream(), content_type='text/event-stream')

def chat_response(user_input:str, session_id:str):
    #max_new_tokens = 256
    #repetition_penalty = 1.2
    #temperature = .4
    #top_k = 50
    #stop_words = [f"{AI_NAME}:", f"{USERNAME}:", "</s>"]
    message_list = get_existing_messages(session_id=session_id)
    message_list.append({"role": "user", "content": f"{user_input}"})
    message_window = 15
    messages = message_list[-message_window:]
    try:
        headers = {
                "Content-Type": "application/json",
                }
        data = {
                "model": MODEL_NAME,
                "messages": messages,
                "response_format": {"type": "json_object"},
                "stream": STREAM,
                }
        res = requests.post(ENDPOINT, headers=headers, stream=STREAM, json=data)
        for word in res.iter_content(chunk_size=5000, decode_unicode=True):     
            print('word', word)
            if word.strip()[6:] != "[DONE]":
                json_response = json.loads(s=word[6:])
                print(json_response)
                if 'content' in json_response['choices'][0]['delta']:
                    content = json_response['choices'][0]['delta']['content']
                    print(content)
                    yield(content)

    except Exception as e:
        response = f"Could not process response.\n\n{e}"
        print("Error: ", e)
        return response

