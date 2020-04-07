from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic
from .forms import TopicForm

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

def new_topic(request):
    # 用户需要用表单提交时用POST，从服务器读取数据页面用GET；
    # 如果请求不是POST，则创建一个新表单，存储在变量 form 中，再通过context字典发送给models
    if request.method != 'POST':
        form = TopicForm()
    else:
        # POST提交数据，则重定向到上一层 topics
        # 使用用户输入的数据（存储在request.POST中）
        form = TopicForm(request.POST)
        # 将form中的数据提交到数据库中，检测是否有效，使用 is_value() 函数来判断填写字段是否完整。
        if form.is_valid():
            # 若填写字段均有效，则调用save()函数进行保存写入数据库。
            form.save()
            # 用reverse()函数获取页面topics的url，返回重定向到topics页面。
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'new_topic.html', context)