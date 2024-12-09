from django.shortcuts import render
import requests

# render start.html page
def start(request):
    return render(request, "start.html")

# render chatbot.html page
def chatbot(request):
    return render(request, "chatbot.html")

def stats(request):
    response = requests.get("http://127.0.0.1:8000/api/num_requests")
    return render(request, 'stats.html', {'response': str(response.content)[18:-2]})
