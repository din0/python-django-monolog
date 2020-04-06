### Django Web App Demo

项目名称: webs

App名称: personal

虚拟环境: venv

开发目的：
1. 个人简历单页页面:index，个人简历展示，内容可通过后台修改；
2. 笔记页面:monolog，前端页面日记随笔记录编辑；
3. 后台:admin，前端页面内容编辑；

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


开发步骤：

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

12. Index主页，添加urls映射,webs/urls.py
    ```python
    from personal import views
    path(r'', views.index, name='index'),
    ```
13. 编写视图，personal/views.py
    ```python
    from django.shortcuts import render
    def index(request):
        return render(request, 'index.html')
    ``` 
14. 编写模板页面，父模板，templates/base.html
    ```html
    <body>
        <h1><a href="{% url 'index' %}">主页</h1>
        {% block content %}{% endblock content %}
    </body>
    ```

15. 编写子模板，templates/index.html
    ```html
    {% extends "base.html" %}
    {% block content %}
        <p>index.html</p>
    {% endblock content %}
    ```
    
16. 显示所有主题页面：Topics，添加urls映射,webs/urls.py
    ```python
    path('topics/', views.topics, name='topics'),
    ```

17. 编写视图，personal/views.py
    ```python
    from .models import Topic
    def topics(request):
        topics = Topic.objects.order_by('date_add')
        context = {'topics': topics}
        return render(request, 'topics.html', context)
    ```

18. 编写模板页面，父模板，templates/base.html
    ```html
    <p><a href="{% url 'topics' %}">主题</a></p>
    ```

19. 编写子模板，templates/index.html
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
    
20. 显示特定主题页面：Topic，添加urls映射,webs/urls.py
    ```python
    path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    ```

21. 编写视图，personal/views.py
    ```python
    def topic(request, topic_id):
        topic = Topic.objects.get(id=topic_id)
        entries = topic.entry_set.order_by('-date_add')
        context = {'topic': topic, 'entries': entries}
        return render(request, 'topic.html', context)
    ```
    
22. 编写父模板，templates/topics.html
    ```html
    {% for topic in topics %}
            <li>
                <a href="{% url 'topic' topic.id %}">{{ topic }}</a>
            </li>
            {% empty %}
            <li>还没有添加主题</li>
            {% endfor %}
    ```

23. 编写子模板，templates/topic.html
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
    
24. 
