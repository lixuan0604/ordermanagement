from django.db import models

from ordermanagement.utils.BaseModel import BaseModel


# Create your models here.


class MasterOrder(models.Model):
    """订单"""

    ORDER_STATUS_ENUM = {
        "notstarted": 1,
        "ongoing": 2,
        "finish": 3,
    }

    ORDER_STATUS_CHOICES = (
        (1, "未开始"),
        (2, "进行中"),
        (3, "完成")
    )

    order_id = models.CharField(max_length=64, verbose_name="订单号")
    customer = models.CharField(max_length=64, verbose_name="客户名称")
    user_id = models.IntegerField(verbose_name="创建用户id")
    uni = models.CharField(max_length=255, verbose_name="学生院校")
    major = models.CharField(max_length=255, verbose_name="专业")
    remark = models.TextField(verbose_name="备注")
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态")
    filepath = models.TextField(verbose_name="文件所在路径")

    class Meta:
        db_table = "tb_master_order"
        verbose_name = '主订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class SubOrder(models.Model):
    """子订单"""
    ORDERID_STATUS_CHOICES = (
        (1, "未开始"),
        (2, "进行中"),
        (3, "完成"),
        (4, "驳回"),
        (5, "质检"),
        (6, "未分配")
    )

    ORDER_STATUS_ENUM = {
        "notstarted": 1,
        "ongoing": 2,
        "finish": 3,
        "reject": 4,
        'inspected': 5,
        "unassign": 6,
    }

    WRITER_STATUS_CHOICES = (
        (1, "未读"),
        (2, "已读")

    )

    WRITER_STATUS_ENUM = {
        "unread": 1,
        "read": 2

    }

    master_order_id = models.IntegerField(verbose_name="主订单id")
    order_id = models.CharField(max_length=255, verbose_name="子订单号")
    uni = models.CharField(max_length=255, verbose_name="申请院校")
    major = models.CharField(max_length=255, verbose_name="专业")
    major_url = models.CharField(max_length=255, verbose_name="专业链接")
    writer_id = models.CharField(max_length=64, verbose_name="写手用户id", default=None)
    writer_name = models.CharField(max_length=255, verbose_name="写手名称")
    plan = models.TextField(verbose_name="职业规划")
    course1 = models.CharField(max_length=255, verbose_name="具体课程")
    course1_url = models.CharField(max_length=255, verbose_name="具体课程链接")
    course2 = models.CharField(max_length=255, verbose_name="具体课程")
    course2_url = models.CharField(max_length=255, verbose_name="具体课程链接")
    course3 = models.CharField(max_length=255, verbose_name="具体课程")
    course3_url = models.CharField(max_length=255, verbose_name="具体课程链接")

    status = models.SmallIntegerField(choices=ORDERID_STATUS_CHOICES, default=1, verbose_name='子订单显示状态')
    writer_status = models.SmallIntegerField(choices=WRITER_STATUS_CHOICES, default=1,
                                             verbose_name='写手显示状态')
    start_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name='任务启动执行时间')
    end_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name='任务预计结束时间')
    text = models.TextField(verbose_name="文本内容", default=None, null=True, blank=True)
    text_comment = models.CharField(max_length=255, verbose_name="驳回原因", default=None, blank=True, null=True, )

    # master_createtime = models.DateTimeField(auto_now_add=True, verbose_name='主订单创建时间')
    # sub_createtime = models.DateTimeField(auto_now_add=True, verbose_name='子订单创建时间')
    # sub_rejecttime = models.DateTimeField(blank=True, null=True, default=None, verbose_name='子订单驳回时间')
    # subop_Modifytime = models.DateTimeField(auto_now=True, verbose_name='op子订单修改时间')
    # sub_finishtime = models.DateTimeField(blank=True, null=True, default=None, verbose_name='子订单修改时间')
    # subwriter_Modifytime = models.DateTimeField(auto_now=True,
    #                                             verbose_name='writer子订单修改时间')

    class Meta:
        db_table = "tb_sub_order"
        verbose_name = '子订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.major
