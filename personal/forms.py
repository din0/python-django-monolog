from django import forms
from .models import Topic, Entry

#定义一个类继承forms.ModelForm
class TopicForm(forms.ModelForm):
    # Meta告诉Django根据哪个model创建表单，表单中包含哪些字段
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

# 创建添加条目表单
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

