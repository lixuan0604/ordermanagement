from django.db import models

from ordermanagement.utils.BaseModel import BaseModel


# Create your models here.


# class Task(BaseModel):
#     """是否完成子订单"""
#
#     writes = models.CharField(max_length=64, verbose_name="写手")
#     master_id = models.CharField(max_length=255, verbose_name="主订单")
#     sub_id = models.CharField(max_length=255, verbose_name="子订单")
#     text = models.TextField(verbose_name="文本内容")
#     status = models.BooleanField(default=0, verbose_name="子订单状态")
#
#     class Meta:
#         db_table = "tb_task"
#         verbose_name = '任务'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.writes
