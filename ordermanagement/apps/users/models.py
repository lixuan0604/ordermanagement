from django.contrib.auth.models import AbstractUser
from django.db import models

from ordermanagement.utils.BaseModel import BaseModel


class User(AbstractUser):
    role = models.CharField(verbose_name="角色", max_length=50, null=True, blank=True)

    class Meta:
        db_table = "tb_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.username


class Roles(models.Model):
    objects = None
    id = models.AutoField(verbose_name="编号", primary_key=True, null=False, blank=False)
    name = models.CharField(verbose_name="名称", max_length=50, null=False, blank=False, unique=False)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True,
                                default=None, related_name='book')
    desc = models.CharField(verbose_name="描述", max_length=200, null=True, blank=True, default=None)

    class Meta:
        db_table = "tb_roles"
        verbose_name = "Roles"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name

# Create your models here.
#
#
# class User(AbstractUser):
#     # id = models.AutoField(verbose_name="id", primary_key=True, null=False, blank=False)
#     name = models.CharField(verbose_name="姓名", max_length=50, null=True, blank=True)
#     status = models.BooleanField(verbose_name="状态", null=False, blank=False, default=1)
#     department = models.CharField(verbose_name="部门", max_length=50, blank=True, null=True, default=None)
#     position = models.CharField(verbose_name="职位", max_length=50, null=True, blank=True, default=None)
#     # 创建时间:
#     create_time = models.DateTimeField(auto_now_add=True,
#                                        verbose_name="创建时间")
#     # 更新时间:
#     update_time = models.DateTimeField(auto_now=True,
#                                        verbose_name="更新时间")
#
#
#     class Meta:
#         db_table = "tb_user"
#         verbose_name = "用户"
#         verbose_name_plural = verbose_name

# def __str__(self):
#     return "%s" % self.name


# 角色信息： Id,name, desc, account
# class Roles(models.Model):
#     id = models.AutoField(verbose_name="编号", primary_key=True, null=False, blank=False)
#     name = models.CharField(verbose_name="名称", max_length=50, null=False, blank=False, unique=False)
#     user = models.ManyToManyField(verbose_name="账号", to=User)
#     desc = models.CharField(verbose_name="描述", max_length=200, null=True, blank=True, default=None)
#
#     class Meta:
#         db_table = "tb_userroles"
#         verbose_name = "Roles"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "%s" % self.name
#
#
# # 顶级菜单：Menu [id, title, icon, order]
# class Menu(models.Model):
#     authName = models.CharField(verbose_name="一级菜单名称", max_length=100, null=False, blank=False, unique=True)
#     icon = models.CharField(verbose_name="图标", max_length=100, null=True, blank=True, default=None)
#     order = models.IntegerField(verbose_name="排序", null=True, blank=True, default=1)
#
#     class Meta:
#         db_table = "tb_menu"
#         verbose_name = "Menu"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "%s" % self.authName
#
#
# class Menuinfo(models.Model):
#     authName = models.CharField(verbose_name="二级菜单名称", max_length=100, null=False, blank=False, unique=True)
#     path = models.CharField(verbose_name="路径", max_length=100, null=True, blank=True, default=None)
#     menu = models.ForeignKey('Menu', on_delete=models.CASCADE, default=0)
#
#     class Meta:
#         db_table = "tb_menuinfo"
#         verbose_name = "Menuinfo"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "%s" % self.authName
#
#
# # 权限： Permission [id, title, url , roles, menu, order]
# class Permission(models.Model):
#     title = models.CharField(verbose_name="名称", max_length=100, null=False, blank=False)
#     url = models.CharField(verbose_name="URL", max_length=200, null=True, blank=True, default=None)
#
#     roles = models.ManyToManyField(verbose_name="角色", to=Roles,  blank=True, default=None)
#     # menu = models.ForeignKey('Menu', on_delete=models.PROTECT, null=True)
#     order = models.IntegerField(verbose_name="排序", unique=False, null=True, blank=True, default=1)
#
#     class Meta:
#         managed = True
#         db_table = "tb_permission"
#         verbose_name = "Permission"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "%s" % self.title
