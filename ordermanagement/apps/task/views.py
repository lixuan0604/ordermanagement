import json, os

from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse
from django.utils.encoding import escape_uri_path
from django.views import View
from order.models import MasterOrder, SubOrder
import datetime

now = datetime.datetime.now()


def file_iterator(file, chunk_size=512):
    with open(file, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


class OrderDetailView(View):
    '''获取订单信息'''

    def get(self, request):
        page = request.GET.get('pagenum')
        limit = request.GET.get('pagesize')
        query = request.GET.get('query')
        userid = request.GET.get('userid')
        rolename = request.GET.get('rolename')
        order_list = []
        if rolename == 'writer':
            obj_sub = SubOrder.objects.filter(writer_id=userid)
        else:
            obj_sub = SubOrder.objects.all()
        paginator = Paginator(obj_sub, limit)
        page_1 = paginator.get_page(page)
        for sub in page_1:
            obj_master = MasterOrder.objects.get(id=sub.master_order_id)
            master_dict = {}
            master_dict['master_id'] = obj_master.id
            master_dict['customer'] = obj_master.customer
            master_dict['university'] = obj_master.uni
            master_dict['major'] = obj_master.major
            master_dict['remark'] = obj_master.remark
            master_dict['filepath'] = obj_master.filepath
            master_dict['order_id'] = obj_master.order_id
            master_dict['children'] = []
            master_dict['children'].append(
                {'id': sub.id, 'university': sub.uni, 'major': sub.major, 'major_url': sub.major_url,
                 'status': sub.status,
                 'course1': sub.course1,
                 'course1_url': sub.course1_url, 'course2': sub.course2, 'course2_url': sub.course2_url,
                 'course3': sub.course3, 'course3_url': sub.course3_url, 'plan': sub.plan,
                 'writer_name': sub.writer_name,
                 'start_time': sub.start_time.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': sub.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')})
            order_list.append(master_dict)
        tmp_data = {}
        for data in order_list:

            if tmp_data.get(data["master_id"]):
                tmp_data[data["master_id"]][0]['children'].append(data['children'][0])
            else:
                tmp_data[data["master_id"]] = []
                tmp_data[data["master_id"]].append(data)
        data_list = []
        for i in tmp_data:
            data_list.append(tmp_data[i][0])
        page_total = paginator.count
        return JsonResponse({'code': 0, 'result': data_list, 'total': page_total, })

    def post(self, request):
        '''下载文件'''
        # 获取请求体中原始的JSON数据
        json_str = request.body
        # 使用json模块将原始的JSON数据转字典
        json_dict = json.loads(json_str)
        masterorder_id = json_dict.get('masterorder_id')
        filepath = json_dict.get('filepath')
        try:
            # obj_master = MasterOrder.objects.get(id=masterorder_id)
            # if eval(obj_master.filepath):
            # for path in eval(obj_master.filepath):
            filename = os.path.basename(filepath)
            file = open(filepath, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Access-Control-Expose-Headers'] = "Content-Disposition, Content-Type"
            response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(filename))
            return response
        except Exception as e:
            return JsonResponse(
                {'code': 1, 'error': "Failed to submit text, the specific reason：" + str(e)})


class SubmitText(View):
    def post(self, request):
        # 获取请求体中原始的JSON数据
        json_str = request.body
        # 使用json模块将原始的JSON数据转字典
        json_dict = json.loads(json_str)
        subid = json_dict.get('subid')
        textarea = json_dict.get('textarea')
        if textarea is None:
            return JsonResponse(
                {'code': 1, 'error': 'Word count not less than 130'})
        text_length = textarea.split()
        if len(text_length) < 130:
            return JsonResponse(
                {'code': 1, 'error': 'Word count not less than 130'})
        try:
            obj_task = SubOrder.objects.filter(id=subid).exists()
            if obj_task:
                obj_sub = SubOrder.objects.get(id=subid)
                if textarea == obj_sub.text:
                    return JsonResponse(
                        {'code': 1, 'error': 'Please check and resubmit the article after it has not been modified'})
                obj_sub.text = textarea
                obj_sub.status = 5
                obj_sub.save()
            else:
                task = SubOrder()
                task.text = textarea
                task.status = 5
                task.save()
        except Exception as e:
            return JsonResponse(
                {'code': 1, 'error': "Failed to submit text, the specific reason：" + str(e)})
        return JsonResponse(
            {'code': 0, 'result': 'Submit text successfully'})

    def get(self, request):
        '''获取文本'''
        subid = request.GET.get('subid')
        text_dict = {}
        try:
            task = SubOrder.objects.filter(id=subid).exists()
            if task:
                obj_task = SubOrder.objects.get(id=subid)
                text_dict['text'] = obj_task.text
            else:
                text_dict['text'] = ''

        except Exception as e:
            return JsonResponse(
                {'code': 1, 'error': "Failed to get text, the specific reason：" + str(e)})
        return JsonResponse(
            {'code': 0, 'result': text_dict})


class OnGoingView(View):
    '''进行中'''

    def get(self, request):
        page = request.GET.get('pagenum')
        limit = request.GET.get('pagesize')
        query = request.GET.get('query')
        userid = request.GET.get('userid')
        rolename = request.GET.get('rolename')
        order_list = []
        if rolename == 'writer':
            obj_sub = SubOrder.objects.filter(writer_id=userid, start_time__lte=datetime.datetime.now()
                                              )
        else:
            obj_sub = SubOrder.objects.filter(start_time__lte=datetime.datetime.now()
                                              )
        paginator = Paginator(obj_sub, limit)
        page_1 = paginator.get_page(page)
        for sub in page_1:
            obj_master = MasterOrder.objects.get(id=sub.master_order_id)
            master_dict = {}
            master_dict['master_id'] = obj_master.id
            master_dict['customer'] = obj_master.customer
            master_dict['university'] = obj_master.uni
            master_dict['major'] = obj_master.major
            master_dict['remark'] = obj_master.remark
            master_dict['filepath'] = obj_master.filepath
            master_dict['order_id'] = obj_master.order_id
            master_dict['children'] = []
            master_dict['children'].append(
                {'id': sub.id, 'university': sub.uni, 'major': sub.major, 'major_url': sub.major_url,
                 'status': sub.status,
                 'course1': sub.course1,
                 'course1_url': sub.course1_url, 'course2': sub.course2, 'course2_url': sub.course2_url,
                 'course3': sub.course3, 'course3_url': sub.course3_url, 'plan': sub.plan,
                 'writer_name': sub.writer_name,
                 'start_time': sub.start_time.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': sub.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')})
            order_list.append(master_dict)

        tmp_data = {}
        for data in order_list:

            if tmp_data.get(data["master_id"]):
                tmp_data[data["master_id"]][0]['children'].append(data['children'][0])
            else:
                tmp_data[data["master_id"]] = []
                tmp_data[data["master_id"]].append(data)
        data_list = []
        for i in tmp_data:
            data_list.append(tmp_data[i][0])
        page_total = paginator.count
        print(data_list)
        return JsonResponse({'code': 0, 'result': data_list, 'total': page_total})


class CheckView(View):
    '''质检'''

    def get(self, request):
        page = request.GET.get('pagenum')
        limit = request.GET.get('pagesize')
        query = request.GET.get('query')
        userid = request.GET.get('userid')
        rolename = request.GET.get('rolename')
        order_list = []
        if rolename == 'writer':
            obj_sub = SubOrder.objects.filter(writer_id=userid, status=5)
        else:
            obj_sub = SubOrder.objects.filter(status=5)
        paginator = Paginator(obj_sub, limit)
        page_1 = paginator.get_page(page)
        for sub in obj_sub:
            obj_master = MasterOrder.objects.get(id=sub.master_order_id)
            master_dict = {}
            master_dict['master_id'] = obj_master.id
            master_dict['customer'] = obj_master.customer
            master_dict['university'] = obj_master.uni
            master_dict['major'] = obj_master.major
            master_dict['remark'] = obj_master.remark
            master_dict['filepath'] = obj_master.filepath
            master_dict['order_id'] = obj_master.order_id
            master_dict['children'] = []
            master_dict['children'].append(
                {'id': sub.id, 'university': sub.uni, 'major': sub.major, 'major_url': sub.major_url,
                 'status': sub.status,
                 'course1': sub.course1,
                 'course1_url': sub.course1_url, 'course2': sub.course2, 'course2_url': sub.course2_url,
                 'course3': sub.course3, 'course3_url': sub.course3_url, 'plan': sub.plan,
                 'writer_name': sub.writer_name,
                 'start_time': sub.start_time.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': sub.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')})
            order_list.append(master_dict)

        tmp_data = {}
        for data in order_list:

            if tmp_data.get(data["master_id"]):
                tmp_data[data["master_id"]][0]['children'].append(data['children'][0])
            else:
                tmp_data[data["master_id"]] = []
                tmp_data[data["master_id"]].append(data)
        data_list = []
        for i in tmp_data:
            data_list.append(tmp_data[i][0])
        page_total = paginator.count
        return JsonResponse({'code': 0, 'result': data_list, 'total': page_total})


class notStartView(View):
    '''未开始'''

    def get(self, request):
        page = request.GET.get('pagenum')
        limit = request.GET.get('pagesize')
        query = request.GET.get('query')
        userid = request.GET.get('userid')
        rolename = request.GET.get('rolename')
        order_list = []
        if rolename == 'writer':
            obj_sub = SubOrder.objects.filter(writer_id=userid, start_time__gte=datetime.datetime.now())
        else:
            obj_sub = SubOrder.objects.filter(start_time__gte=datetime.datetime.now())
        paginator = Paginator(obj_sub, limit)
        page_1 = paginator.get_page(page)
        for sub in page_1:
            obj_master = MasterOrder.objects.get(id=sub.master_order_id)
            master_dict = {}
            master_dict['master_id'] = obj_master.id
            master_dict['customer'] = obj_master.customer
            master_dict['university'] = obj_master.uni
            master_dict['major'] = obj_master.major
            master_dict['remark'] = obj_master.remark
            master_dict['filepath'] = obj_master.filepath
            master_dict['order_id'] = obj_master.order_id
            master_dict['children'] = []
            master_dict['children'].append(
                {'id': sub.id, 'university': sub.uni, 'major': sub.major, 'major_url': sub.major_url,
                 'status': sub.status,
                 'course1': sub.course1,
                 'course1_url': sub.course1_url, 'course2': sub.course2, 'course2_url': sub.course2_url,
                 'course3': sub.course3, 'course3_url': sub.course3_url, 'plan': sub.plan,
                 'writer_name': sub.writer_name,
                 'start_time': sub.start_time.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': sub.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')})
            order_list.append(master_dict)
        tmp_data = {}
        for data in order_list:

            if tmp_data.get(data["master_id"]):
                tmp_data[data["master_id"]][0]['children'].append(data['children'][0])
            else:
                tmp_data[data["master_id"]] = []
                tmp_data[data["master_id"]].append(data)
        data_list = []
        for i in tmp_data:
            data_list.append(tmp_data[i][0])
        page_total = paginator.count
        print(page_total)
        return JsonResponse({'code': 0, 'total': page_total, 'result': data_list})


class RejectView(View):
    '''驳回'''

    def get(self, request):
        page = request.GET.get('pagenum')
        limit = request.GET.get('pagesize')
        query = request.GET.get('query')
        userid = request.GET.get('userid')
        rolename = request.GET.get('rolename')
        order_list = []
        if rolename == 'writer':
            obj_sub = SubOrder.objects.filter(writer_id=userid, status=4)
        else:
            obj_sub = SubOrder.objects.filter(status=4)
        paginator = Paginator(obj_sub, limit)
        page_1 = paginator.get_page(page)
        for sub in page_1:
            obj_master = MasterOrder.objects.get(id=sub.master_order_id)
            master_dict = {}
            master_dict['master_id'] = obj_master.id
            master_dict['customer'] = obj_master.customer
            master_dict['university'] = obj_master.uni
            master_dict['major'] = obj_master.major
            master_dict['remark'] = obj_master.remark
            master_dict['filepath'] = obj_master.filepath
            master_dict['order_id'] = obj_master.order_id
            master_dict['children'] = []
            master_dict['children'].append(
                {'id': sub.id, 'university': sub.uni, 'major': sub.major, 'major_url': sub.major_url,
                 'status': sub.status,
                 'course1': sub.course1,
                 'course1_url': sub.course1_url, 'course2': sub.course2, 'course2_url': sub.course2_url,
                 'course3': sub.course3, 'course3_url': sub.course3_url, 'plan': sub.plan,
                 'writer_name': sub.writer_name,
                 'reject': sub.text_comment, 'start_time': sub.start_time.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': sub.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')})
            order_list.append(master_dict)
        tmp_data = {}
        for data in order_list:

            if tmp_data.get(data["master_id"]):
                tmp_data[data["master_id"]][0]['children'].append(data['children'][0])
            else:
                tmp_data[data["master_id"]] = []
                tmp_data[data["master_id"]].append(data)
        data_list = []
        for i in tmp_data:
            data_list.append(tmp_data[i][0])
        page_total = paginator.count
        return JsonResponse({'code': 0, 'result': data_list, 'total': page_total})


class FinishView(View):
    '''完成'''

    def get(self, request):
        page = request.GET.get('pagenum')
        limit = request.GET.get('pagesize')
        query = request.GET.get('query')
        userid = request.GET.get('userid')
        rolename = request.GET.get('rolename')
        order_list = []
        if rolename == 'writer':
            obj_sub = SubOrder.objects.filter(writer_id=userid, status=3)
        else:
            obj_sub = SubOrder.objects.filter(status=3)
        paginator = Paginator(obj_sub, limit)
        page_1 = paginator.get_page(page)
        for sub in page_1:
            obj_master = MasterOrder.objects.get(id=sub.master_order_id)
            master_dict = {}
            master_dict['master_id'] = obj_master.id
            master_dict['customer'] = obj_master.customer
            master_dict['university'] = obj_master.uni
            master_dict['major'] = obj_master.major
            master_dict['remark'] = obj_master.remark
            master_dict['filepath'] = obj_master.filepath
            master_dict['order_id'] = obj_master.order_id
            master_dict['children'] = []
            master_dict['children'].append(
                {'id': sub.id, 'university': sub.uni, 'major': sub.major, 'major_url': sub.major_url,
                 'status': sub.status,
                 'course1': sub.course1,
                 'course1_url': sub.course1_url, 'course2': sub.course2, 'course2_url': sub.course2_url,
                 'course3': sub.course3, 'course3_url': sub.course3_url, 'plan': sub.plan,
                 'writer_name': sub.writer_name,
                 'start_time': sub.start_time.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': sub.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')})
            order_list.append(master_dict)
        tmp_data = {}
        for data in order_list:

            if tmp_data.get(data["master_id"]):
                tmp_data[data["master_id"]][0]['children'].append(data['children'][0])
            else:
                tmp_data[data["master_id"]] = []
                tmp_data[data["master_id"]].append(data)
        data_list = []
        for i in tmp_data:
            data_list.append(tmp_data[i][0])
        page_total = paginator.count
        return JsonResponse({'code': 0, 'result': data_list, 'total': page_total})
