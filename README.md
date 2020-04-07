### Django Web App Demo

项目名称: webs

App名称: personal

虚拟环境: venv

开发目的：
1. 个人简历单页页面：index，个人简历展示，内容可通过后台修改；
2. 笔记页面：monolog，前端页面日记随笔记录编辑；
3. 后台：admin，前端页面内容编辑；

开发工具：
1. Python-3.7.6
2. Django 3.0
3. Pycharm Pro 2019.3.4
4. Jupyter
5. Chrome

项目结构：
1. webs
2. personal
3. templates
4. manage.py


#### 开发步骤：

A. 准备：

1. pycharm新建project，设置运行环境及应用名称；
2. 默认前端页面：http://127.0.0.1:8000/
   
   问题：端口被占用 “That port is already in use”
   
   解决：执行```python manage.py runserver 8001```
3. 后台admin：http://127.0.0.1:8000/admin/
4. 数据库：使用 db.sqlite3，webs/webs/settings.py
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 
        }
    }
    ```
5. 创建数据库：
    ```$ python3 manage.py migrate```

B. 开发

6. 定义模型 Topic webs/personal/models.py，Topic类只有两个属性
    ```python
    class Topic(models.Model):
    # 定义log主题，长度200字符
    text = models.CharField(max_length=200)
    # 定义添加的时间为当前时间
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 返回模型字符串
        return self.text
    ```
7. 更新数据库，加载Topic.models，为Topic创建一个表

    ```$ python3 manage.py makemigrations personal```
    
    数据库迁移：
    
    ```$ python3 manage.py migrate```
    
    每当需要修改管理数据时，需要执行三个步骤：
    a. 修改 models.py
    b. 调用makemigrations
    c. 迁移项目 migrate

8. 创建admin账户
    ```
    $ python3 manage.py createsuperuser
    ```
    按照提示依次输入：用户名，Email，密码；
    创建完成后即可通过后台登录
    
9. 向后台添加Models，webs/personal/admin.py
    ```python
    from django.contrib import admin
    from personal.models import Topic
    admin.site.register(Topic)
    ```
    此时进入后台即可看到新增加的model，Personal/Topics
    
10. 定义模型 Entry webs/personal/models.py
    ```python
    class Entry(models.Model):
    # Topic 下的条目
    # 外键引用了数据库中的一条记录，此处为 Topic，将每条记录关联到特定的主题。
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date_add = models.DateTimeField(auto_now_add=True)

    # Meta用于存储管理模型的额外信息，设置特殊属性，让Django在需要时使用Entries表示多个条目。
    class Mate:
        verbose_name_plural = 'entries'

    def __str__(self):
        if len(self.text) >= 50:
            return self.text[:50] + "..."
        else:
            return self.text
    ```
    迁移模型，使用 makemigrations & migrate
    
11. 向后台添加Model，webs/personal/admin.py
    ```python
    from personal.models import Topic, Entry
    admin.site.register(Entry)
    ```
    
C. 前端页面：

12. Index主页

    添加urls映射,webs/urls.py
    ```python
    from personal import views
    path(r'', views.index, name='index'),
    ```
    编写视图，personal/views.py
    ```python
    from django.shortcuts import render
    def index(request):
        return render(request, 'index.html')
    ``` 
    编写模板页面，父模板，templates/base.html
    ```html
    <body>
        <h1><a href="{% url 'index' %}">主页</h1>
        {% block content %}{% endblock content %}
    </body>
    ```
    编写子模板，templates/index.html
    ```html
    {% extends "base.html" %}
    {% block content %}
        <p>index.html</p>
    {% endblock content %}
    ```
    
13. 显示所有主题页面：Topics

    添加urls映射,webs/urls.py
    ```python
    path('topics/', views.topics, name='topics'),
    ```
    编写视图，personal/views.py
    ```python
    from .models import Topic
    def topics(request):
        topics = Topic.objects.order_by('date_add')
        context = {'topics': topics}
        return render(request, 'topics.html', context)
    ```
    编写模板页面，父模板，templates/base.html
    ```html
    <p><a href="{% url 'topics' %}">主题</a></p>
    ```
    编写子模板，templates/index.html
    ```html
    {% extends "base.html" %}
    {% block content %}
        <p>Topics</p>
        <ul>
            {% for topic in topics %}
            <li>{{ topic }}</li>
            {% empty %}
            <li>还没有添加主题</li>
            {% endfor %}
        </ul>
    {% endblock content %}
    ```
    
14. 显示特定主题页面：Topic

    添加urls映射,webs/urls.py
    ```python
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    ```
    编写视图，personal/views.py
    ```python
    def topic(request, topic_id):
        topic = Topic.objects.get(id=topic_id)
        entries = topic.entry_set.order_by('-date_add')
        context = {'topic': topic, 'entries': entries}
        return render(request, 'topic.html', context)
    ```
    编写父模板，templates/topics.html
    ```html
    {% for topic in topics %}
            <li>
                <a href="{% url 'topic' topic.id %}">{{ topic }}</a>
            </li>
            {% empty %}
            <li>还没有添加主题</li>
            {% endfor %}
    ```
    编写子模板，templates/topic.html
    ```html
    {% extends 'base.html' %}
    {% block content %}
        <p>{{ topic }}</p>
        <p>内容：</p>
        <ul>
            {% for entry in entries %}
            <li>
                <p>{{ entry.date_add|date:'M d, Y H:i' }}</p>
                <p>{{ entry.text|linebreaks }}</p>
            </li>
            {% empty %}
            <li>该主题还没有内容</li>
            {% endfor %}
        </ul>
    {% endblock content %}
    ```

D. 前端编辑页面，用户可在页面编辑

15. 添加新主题 new_topic

    创建表单 webs/personal/forms.py
    ```python
    from django import forms
    from .models import Topic
    
    #定义一个类继承forms.ModelForm
    class TopicForm(forms.ModelForm):
        # Meta告诉Django根据哪个model创建表单，表单中包含哪些字段
        class Meta:
            model = Topic
            fields = ['text']
            labels = {'text': ''}
    ```
    创建 new_topic
    urls.py
    ```python
    path('new_topic/', views.new_topic, name='new_topic'),
    ```
    views.py
    ```python
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
    ```
    new_topic.html
    ```html
    {% extends "base.html" %}
    {% block content %}
        <p>添加新主题：</p>
        <form action="{% url 'new_topic' %}" method="post">
    <!--        模板标签防止攻击者利用表单获取对服务器未经授权的访问，跨站请求伪造攻击-->
            {% csrf_token %}
    <!--        .as_p让Django以段落格式渲染所有表单元素-->
            {{ form.as_p }}
            <button name="submit">提交</button>
        </form>
    {% endblock content %}
    ```
    topics.html
    ```html
    <a href="{% url 'new_topic' %}">添加新主题</a>
    ```

16. 添加新条目 new_entry

    创建表单：forms.py
    ```python
    from .models import Topic, Entry
    # 创建添加条目表单
    class EntryForm(forms.ModelForm):
        class Meta:
            model = Entry
            fields = ['text']
            labels = {'text': ''}
            widgets = {'text': forms.Textarea(attrs={'cols': 80})}
    ```
    urls.py
    ```python
    re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    ```
    views.py
    ```python
    from .forms import TopicForm, EntryForm
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
    ```
    new_entry.html
    ```html
    {% extends "base.html" %}
    {% block content %}
        <p>主题：<a href="{% url 'topic' topic.id %}">{{ topic }}</a></p>
        <p>添加新的条目：</p>
        <form action="{% url 'new_entry' topic.id %}" method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button name="submit">提交</button>
        </form>
    {% endblock content %}
    ```
    topic.html 添加链接
    ```html
    <p>主题：{{ topic }}</p>
    <p>内容：</p>
    <p><a href="{% url 'new_entry' topic.id %}">添加新条目</a></p>
    ```

17. 编辑条目 edit_entry

    urls.py
    ```python
    re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    ```
    views.py
    ```python
    from .models import Topic, Entry
    def edit_entry(request, entry_id):
        # 获取需要修改的条目对象，以及对应的主题
        entry = Entry.objects.get(id=entry_id)
        topic = entry.topic
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
    ```
    edit_entry.html
    ```html
    {% extends "base.html" %}
    {% block content %}
        <p>主题：<a href="{% url 'topic' topic.id %}">{{ topic }}</a></p>
        <p>编辑条目：</p>
        <form action="{% url 'edit_entry' entry.id %}" method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button name="submit">保存</button>
        </form>
    {% endblock content %}
    ```
    topic.html
    ```html
    <p><a href="{% url 'edit_entry' entry.id %}">编辑该条目</a></p>
    ```

E. 用户账户系统

18. 登录&注销

    创建一个新的APP：users
    ```
    python3 manage.py startapp users
    ```
    将users添加到setting.py中
    ```python
    INSTALLED APPS=('users',)
    ```
    urls.py
    ```python
    from django.contrib.auth.views import LoginView
    urlpatterns = [
        path('login/', LoginView.as_view(template_name='login.html'), name='login'),
        path('logout/', views.logout_view, name='logout'),
    ]
    ```
    views.py
    ```python
    def logout_view(request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    ```
    login.html
    ```html
    {% extends "base.html" %}
    {% block content %}
        {% if form.errors %}
            <p>Your username and password didn't match. Please try again.</p>
        {% endif %}
        <form method="post" action="{% url 'login' %}" class="form">
            {% csrf_token %}
            {{ form.as_p }}
            <button name="submit">Login</button>
            <input type="hidden" name="next" value="{% url 'index' %}" />
        </form>
    {% endblock content %}
    ```
    base.html
    ```html
    <p>
        {% if user.is_authenticated %}
            Hello, {{ user.username }}.
            <a href="{% url 'logout' %}">注销</a>
        {% else %}
            <a href="{% url 'login' %}">log in</a>
        {% endif %}
    </p>
    ```
19. 注册

    urls.py
    ```python
    path('register/', views.register, name='register'),
    ```
    views.py
    ```python
    from django.contrib.auth import login, logout, authenticate
    from django.contrib.auth.forms import UserCreationForm
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
    ```
    register.html
    ```html
    {% extends "base.html" %}
    {% block content %}
        <form method="post" action="{% url 'register' %}">
            {% csrf_token %}
            {{ form.as_p }}
            <button name="submit">register</button>
            <input type="hidden" name="next" value="{% url 'index' %}" />
        </form>
    {% endblock content %}
    ```
    base.html
    ```html
    {% else %}
        <a href="{% url 'register' %}">注册</a>
        <a href="{% url 'login' %}">登录</a>
    {% endif %}
    ```
    
20. 用户数据权限设置

    限制访问：@login_required
    views.py
    ```python
    from django.contrib.auth.decorators import login_required
    @login_required
    def topics(request):
    ```
    当未登录时，返回login页面
    setting.py
    ```python
    LOGIN_URL = '/login/'
    ```

21. 数据关联到用户

    personal/models.py
    ```
    from django.contrib.auth.models import User
    class Topic(models.Model):
        # 增加关联到对应用户的外键
        owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ```
    迁移数据库：
    ```python
    $ python3 manage.py makemigrations personal
    $ python3 manage.py migrate
    ```

22. 只允许当前用户访问自己创建的内容

    views.py
    ```python
    from django.http import HttpResponseRedirect, Http404
    def topics(request):
        # filter()过滤用户
        topics = Topic.objects.filter(owner=request.user).order_by('date_add')
        ...
    def topic(request, topic_id):
        topic = Topic.objects.get(id=topic_id)
        # 确认请求内容属于当前账户
        if topic.owner != request.user:
            raise Http404
        ...
    def edit_entry(request, entry_id):
        # 获取需要修改的条目对象，以及对应的主题
        entry = Entry.objects.get(id=entry_id)
        topic = entry.topic
    
        if topic.owner != request.user:
            raise Http404
        ...
    def new_topic(request):
        else:
            ...
            if form.is_valid():
                # 添加到对应的用户主题
                new_topic = form.save(commit=False)
                new_topic.owner = request.user
                new_topic.save()
                # 若填写字段均有效，则调用save()函数进行保存写入数据库。
                # form.save()
            ...
    ```

F. 页面样式设置（bootstrap3）

23. 安装 django-bootstrap3
    ```python
    # 注意：这里使用python3 -m pip，因为之前直接用pip3 install，有时会出现由于writable的情况，安装成功，但是无法调用。
    $ python3 -m pip install django-bootstrap3
    ```
    配置：setting.py
    ```python
    INSTALLED_APPS = [
        'bootstrap3',
    ]
    # 将jQuery库加入
    BOOTSTRAP3 = {
        'include_jquery': True,
    }
    ```

24. 修改页面样式
base.html
```html
# 顶部添加
{% load bootstrap3 %}

#<head>中添加css和js调用
{% bootstrap_css %}
{% bootstrap_javascript %}
```
导航：
```html
<nav class="navbar navbar-default">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed"
                data-toggle="collapse" data-target="#navbar"
                aria-expanded="false" aria-controls="navbar">
            </button>
            <a class="navbar-brand" href="{% url 'index' %}">
                Learning Log
            </a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="{% url 'topics' %}">主题</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                {% if user.is_authenticated %}
                    <li><a>hi, {{ user.username }}.</a></li>
                    <li><a href="{% url 'logout' %}">注销</a></li>
                {% else %}
                    <li><a href="{% url 'register' %}">注册</a></li>
                     <li><a href="{% url 'login' %}">登录</a></li>
                {% endif %}
            </ul>
    </div>
</nav>
```
页面主体；
```html
<div class="container">
    <div class="page-header">
        {% block header %}{% endblock header %}
    </div>
    <div>
        {% block content %}{% endblock content %}
    </div>
</div>
```




G. 项目部署

Git，选择阿里云或者Github

```
$ git init
$ echo python-django-monolog" >> README.md
$ git commit -m "first commit"
$ git git remote add origin https://github.com/xxxx/python-django-monolog.git
$ git push -u origin master
# 输入用户名和密码
# 开始执行
日常更新发布
$ git add .
$ git commit -m "notes"
$ git push
```


