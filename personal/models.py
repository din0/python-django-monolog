from django.db import models

class Topic(models.Model):
    # 定义log主题，长度200字符
    text = models.CharField(max_length=200)
    # 定义添加时间
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 返回模型字符串
        return self.text

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