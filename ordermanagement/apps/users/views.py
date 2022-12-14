from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from users.models import User, Roles
import datetime
import json

# Create your views here.


import pymysql


# def get_connection():
#     # 连接数据库
#     connect = pymysql.Connect(
#         host='172.16.10.7',
#         port=3306,
#         user='product',
#         passwd='pl,okm098',
#         db='ordermanagement_test',
#         charset='utf8'
#     )
#     # 获取游标(指定获取的数据格式，这里设定返回dict格式)
#     return connect, connect.cursor(cursor=pymysql.cursors.DictCursor)
#
#
# def select_all(sql, args=None):
#     # 查询全部
#     conn, cursor = get_connection()
#     cursor.execute(sql, args)
#     results = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     # 返回查询结果
#     return results


class Login(View):
    """登录"""

    def post(self, request):
        # 获取请求体中原始的JSON数据
        json_str = request.body
        # 使用json模块将原始的JSON数据转字典
        json_dict = json.loads(json_str)
        username = json_dict.get('username')
        password = json_dict.get('password')
        try:
            users = User.objects.get(username=username, password=password)
            # 判断是否禁用
            if bool(users.is_active) == False:
                return JsonResponse(
                    {'code': 1, 'error': 'The account has been disabled, please contact the administrator！'})
            # 判断用户是否存在
            if users is None:
                return JsonResponse({'code': 1, 'error': 'User information does not exist！'})

            # 登录成功 写入当前时间
            users.last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            users.save()
            # ===== 获取返回数据 ====
            res_data = {
                'id': users.id,
                'username': users.username,
                'create_time': users.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
                'last_login': users.last_login,
                'rolename': users.role
            }
            login(request, users)
            return JsonResponse({'code': 0, 'data': res_data})
        except Exception as e:
            return JsonResponse({'code': 1, 'error': 'Incorrect username or password:' + str(e)})

    def get(self, request):
        """获取所有用户"""
        page = request.GET.get('pagenum')
        limit = request.GET.get('pagesize')
        query = request.GET.get('query')
        rolename = request.GET.get('rolename')
        result = []
        roles = Roles.objects.all()
        roles_list = []
        for role in roles:
            if rolename == 'op':
                roles_list = ['writer']
                break
            roles_list.append(role.name)
        if query:
            all_count = User.objects.filter(Q(username__icontains=query) | Q(role__icontains=query)).order_by("id")
        else:
            all_count = User.objects.all()
        paginator = Paginator(all_count, limit)
        page_1 = paginator.get_page(page)
        for que in page_1:
            # user_obj = User.objects.get(role=que.role)
            user_obj = Roles.objects.get(name=que.role)
            role_dict = {}
            query_info = {}
            query_info["id"] = que.id
            query_info["role"] = que.role
            query_info["roleid"] = user_obj.id
            query_info["username"] = que.username
            query_info["password"] = que.password
            query_info["createtime"] = que.date_joined.strftime("%Y-%m-%d %H:%M:%S")
            query_info["last_login"] = que.last_login.strftime("%Y-%m-%d %H:%M:%S")
            query_info["status"] = que.is_active
            result.append(query_info)

        if rolename == 'op':
            result = [item for item in result if item['role'] != 'admin' and item['role'] != 'op']
            return JsonResponse({'code': 0, 'result': result, 'total': len(result), "roles": roles_list})
        else:
            page_total = paginator.count
            return JsonResponse({'code': 0, 'result': result, 'total': page_total, "roles": roles_list})

    def put(self, request):
        '''更改用户状态'''
        username = request.GET.get('username')
        status = request.GET.get('status')
        user = User.objects.get(username=username)
        if user:
            try:
                if status == 'true':
                    user.is_active = True
                else:
                    user.is_active = False
                user.save()
                return JsonResponse({'code': 0, 'success': 'Change user status successfully!'})
            except Exception as e:
                return JsonResponse({'code': 1, 'error': 'Failed to change user status!'})
        else:
            return JsonResponse({'code': 1, 'error': 'The current user to modify the status does not exist!'})


class CreateUser(View):
    # 创建用户
    def post(self, request):
        # 获取请求体中原始的JSON数据
        json_str = request.body
        # 使用json模块将原始的JSON数据转字典
        json_dict = json.loads(json_str)
        role = json_dict.get('role')
        username = json_dict.get('username')
        password = json_dict.get('password')
        # rolename = json_dict.get('rolename')
        # loginusername = json_dict.get('loginusername')

        # 判断账户是否存在
        is_user = User.objects.filter(username=username).exists()
        if is_user:
            return JsonResponse(
                {'code': 1, 'error': 'This account already exists, please re-enter！'})

        else:
            try:
                # if rolename == 'op' and role == 'admin':
                #     return JsonResponse(
                #         {'code': 1, 'error': 'No permission to create admin user！'})

                # 添加账号
                User.objects.create(
                    username=username,
                    password=password,
                    role=role,
                    is_active=True,
                    date_joined=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    last_login=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                # if role:
                #     # 1) 获取当前的账号对象 ！
                #     user_obj = User.objects.filter(username=username).first()
                #     roles_obj = Roles.objects.filter(name=role).first()
                #     # 添加映射
                #     roles_obj.user.add(user_obj)

            except Exception as e:
                return JsonResponse(
                    {'code': 1, 'error': "Adding an account appears abnormal, the specific reason：" + str(e)})
        return JsonResponse(
            {'code': 0, 'result': 'Role added successfully'})

    def put(self, request):
        '''修改用户角色信息'''
        # 获取请求体中原始的JSON数据
        json_str = request.body
        # 使用json模块将原始的JSON数据转字典
        json_dict = json.loads(json_str)
        username = json_dict.get('username')
        role = json_dict.get('role')
        newrole = json_dict.get('newrole')
        # conn, cursor = get_connection()
        try:
            # 当前用户名
            user_obj = User.objects.get(username=username)
            user_obj.role = newrole
            user_obj.save()
            # # 当前角色
            # roles_obj = Roles.objects.get(name=role)
            # # 新角色
            # newroles_obj = Roles.objects.get(name=newrole)
            # # 查询全部
            # sql = "update tb_userroles_user set roles_id=%s where roles_id= %s and user_id=%s" % (
            #     newroles_obj.id, roles_obj.id, user_obj.id)
            # cursor.execute(sql)
            # conn.commit()
        except Exception as e:
            # 发生错误时回滚
            # conn.rollback()
            return JsonResponse(
                {'code': 1, 'error': "Failed to modify character, the specific reason：" + str(e)})
        return JsonResponse(
            {'code': 0, 'result': 'Modify character successfully'})

    def delete(self, request):
        '''删除用户'''
        # 获取请求体中原始的JSON数据
        json_str = request.body
        # 使用json模块将原始的JSON数据转字典
        json_dict = json.loads(json_str)
        username = json_dict.get('username')
        try:
            User.objects.filter(username=username).delete()
        except Exception as e:
            return JsonResponse(
                {'code': 1, 'error': "Failed to delete user, the specific reason：" + str(e)})
        return JsonResponse(
            {'code': 0, 'result': 'delete user successfully'})


# class MenuView(View):
#     """获取菜单"""
#
#     def get(self, request):
#         menulist = []
#         menu_obj = Menu.objects.all()
#         for menu in menu_obj:
#             menuinfo_list = []
#             menu_dict = {}
#             menu_dict['id'] = menu.id
#             menu_dict['authName'] = menu.authName
#             menu_dict['children'] = menuinfo_list
#             menuinfo_obj = Menuinfo.objects.filter(menu_id=menu.id)
#             for menuinfo in menuinfo_obj:
#                 menuinfo_dict = {}
#                 menuinfo_dict['id'] = menuinfo.id
#                 menuinfo_dict['authName'] = menuinfo.authName
#                 menuinfo_dict['path'] = menuinfo.path
#                 menuinfo_list.append(menuinfo_dict)
#
#             menulist.append(menu_dict)
#         return JsonResponse(
#             {'data': menulist, "meta": {
#                 "msg": '获取菜单列表成功',
#                 "status": 200
#             }})


class RoleView(View):
    '''获取角色'''

    def get(self, request):
        roles = Roles.objects.all()
        rolelist = []
        for role in roles:
            role_dict = {}
            role_dict['id'] = role.id
            role_dict['name'] = role.name
            role_dict['desc'] = role.desc
            rolelist.append(role_dict)

        # menu_obj = Menu.objects.all()
        # obj_permission = Permission.objects.all()
        # data = []
        # for menu in menu_obj:
        #     menu_dict = {}
        #     menu_dict['id'] = menu.id
        #     menu_dict['title'] = menu.authName
        #     menu_dict['children'] = []
        #     for permission in obj_permission:
        #         if permission.menu_id == menu.id:
        #             menu_dict['children'].append({'id':permission.id,'title':permission.title,'url':permission.url,'pid':menu.id,'ptitle':menu.authName})
        #
        #     data.append(menu_dict)
        # print('data',data)
        return JsonResponse(
            {'data': rolelist, "meta": {
                "msg": '获取菜单列表成功',
                "status": 200
            }})


# class PerssionView(View):
#     def get(self, request):
#         try:
#             per_obj = Menu.objects.all()
#             permission_list = []
#             for per in per_obj:
#                 per_dict = {}
#                 per_dict['id'] = per.id
#                 per_dict['authName'] = per.authName
#                 per_obj1 = Menuinfo.objects.filter(menu_id=per.id)
#                 for per1 in per_obj1:
#                     per1_dict = {}
#                     per1_dict['id'] = per1.id
#                     per1_dict['authName'] = per1.authName
#                     per1_dict['pid'] = per.id
#                     per_dict['children'] = [per1_dict]
#                     per1_dict['children'] = []
#                     per_obj2 = Menuinfo.objects.filter(menu_id=per1.id)
#                     for per2 in per_obj2:
#                         per1_dict['children'].append(
#                             {'id': per2.id, 'authName': per2.authName, 'pid': str(per.id) + '' + str(per1.id)})
#                 permission_list.append(per_dict)
#         except Exception as e:
#             # 如果报错, 则返回错误原因:
#             return JsonResponse({'status': 400,
#                                  'errmsg': '角色信息错误'})
#         print(permission_list)
#         return JsonResponse({"status": 200,
#                              'errmsg': 'OK',
#                              'data': permission_list})


class getUserView(View):
    # 根据角色id获取该角色下所有用户
    def post(self, request):
        role_id = request.POST.get('id')
        obj_role = Roles.objects.get(id=role_id)
        # obj_user = obj_role.user.all()
        obj_user = User.objects.filter(role=obj_role.name)
        user_list = []
        try:
            for user in obj_user:
                user_dict = {}
                user_dict['id'] = user.id
                user_dict['username'] = user.username
                user_dict['teacher'] = str(user.id) + '-' + user.username
                user_list.append(user_dict)
        except Exception as e:
            return JsonResponse({"code": 400,
                                 'error': "Query failure, the specific reason：" + str(e)
                                 })
        return JsonResponse({"code": 200,
                             'errmsg': 'OK',
                             'data': user_list})
