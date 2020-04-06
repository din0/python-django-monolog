from django.shortcuts import render
from .models import Topic

def index(request):
    return render(request, 'index.html')

def topics(request):
    topics = Topic.objects.order_by('date_add')
    context = {'topics': topics}
    return render(request, 'topics.html', context)

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_add')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'topic.html', context)