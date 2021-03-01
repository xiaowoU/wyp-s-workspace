from django.db import models

class BaseModel(models.Model):
    '''模型抽象基类'''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True)

    class Meta:
        abstract = True # 说明是一个抽象模型类


class DataModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True)

    class Meta:
        abstract = True