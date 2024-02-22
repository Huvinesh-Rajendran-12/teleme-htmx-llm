import os
from django.shortcuts import render
import requests

from .models import Message

ENDPOINT = os.getenv('ENDPOINT', '')
MODEL_NAME = os.getenv('MODEL_NAME', '')
STREAM = True if os.getenv('STREAM', 'False').lower() == 'true' else False

# Create your views here.
def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        llm_message = llm_generate_response(user_input=user_message)
        Message.objects.create(user_message=user_message, llm_message=llm_message)

    messages = Message.objects.all()
    return render(request, 'chat.html', {'messages':messages})

def llm_generate_response(user_input:str):
    # Set up the API endpoint and headers
    print('ENDPOINT', ENDPOINT)
    print('MODEL_NAME', MODEL_NAME)
    print('STREAM', STREAM)
    headers = {
        "Content-Type": "application/json",
    }

    # Data payload
    messages = get_existing_messages()
    messages.append({"role": "user", "content": f"{user_input}"})
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "stream": STREAM
    }
    response = requests.post(ENDPOINT, headers=headers, stream=STREAM, json=data)
    response_data = response.json()
    print(f'{response_data = }')
    ai_message = response_data['choices'][0]['message']['content']
    print('ai message', ai_message)
    return ai_message

def get_existing_messages() -> list:
    """
    Get all messages from the database and format them for the API.
    """
    formatted_messages = []

    for message in Message.objects.values('user_message', 'llm_message'):
        formatted_messages.append({"role": "user", "content": message['user_message']})
        formatted_messages.append({"role": "assistant", "content": message['llm_message']})

    return formatted_messages
