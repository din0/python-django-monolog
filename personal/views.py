from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

@login_required
def topics(request):
    # filter()过滤用户
    topics = Topic.objects.filter(owner=request.user).order_by('date_add')
    context = {'topics': topics}
    return render(request, 'topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    # 确认请求内容属于当前账户
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_add')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'topic.html', context)

@login_required
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
            # 添加到对应的用户主题
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # 若填写字段均有效，则调用save()函数进行保存写入数据库。
            # form.save()
            # 用reverse()函数获取页面topics的url，返回重定向到topics页面。
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    # 处理表单数据时，需要知道针对的是哪个主题，所以用topic_id来获得对应的主题
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 船体了实参 commit=False， 让Django创建新的条目对象并存储于new_entry中，但不保存到数据库中。
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # 调用reverse()时，需要提供两个实参，生成URL的名称，args列表包含在URL中的所有实参，此处只有一个topic_id元素
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    # 获取需要修改的条目对象，以及对应的主题
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        # 根据表单里已有内容进行修改
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'edit_entry.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username = new_user.username, password = request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    context = {'form': form}
    return render(request, 'register.html', context)