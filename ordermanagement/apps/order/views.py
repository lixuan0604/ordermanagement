import datetime
import os.path
import re
import time

import docx
from django.utils.encoding import escape_uri_path


from django.views import View
from django.http import JsonResponse
import json
# Create your views here.
from order.models import MasterOrder, SubOrder
from users.models import User
from pathlib import Path
from django.http import StreamingHttpResponse


def UTC2BJS(UTC):
    print('utc_1:',UTC)
    UTC_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    BJS_format = "%Y-%m-%d %H:%M:%S"
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    # print('offset:', type(offset))
    UTC = datetime.datetime.strptime(UTC,UTC_format)
    #格林威治时间+8小时变为北京时间
    # BJS = UTC + datetime.timedelta(hours=8)
    BJS = UTC + offset
    BJS = BJS.strftime(BJS_format)
    return BJS


class InspectdSubOrderView(View):
    """
    质检
    """

    def post(self, request):
        try:
            query_dict = request.POST
            status = query_dict['status']
            id = query_dict['id']
            text_comment = query_dict['comment']
            SubOrder.objects.filter(id=id).update(status=status, text_comment=text_comment)
            return JsonResponse({'code': 200, 'msg': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'msg': str(e)})


class CreateMasterOrderView(View):
    """创建主订单"""

    def post(self, request):
        try:
            query_dict = request.POST
            customer = query_dict['customer']
            uni = query_dict['uni']
            major = query_dict['major']
            remark = query_dict['remark']
            user_id = query_dict['userid']
            order_id = query_dict['orderid']
            files = request.FILES.getlist('files')
            print(files)
            try:
                id = query_dict['id']
                if id:
                    print('更改主订单')
                    # MasterOrder.objects.filter(id=id).update()
            except Exception as e:
                print(e)
                print('创建主订单')
                m = MasterOrder.objects.create(order_id=order_id, customer=customer, uni=uni, major=major,
                                               remark=remark,
                                               user_id=user_id)
                id = m.id
            BASE_DIR = os.path.join(Path(__file__).resolve().parent.parent.parent.parent, 'statics')
            path_folder = os.path.join(BASE_DIR, str(customer) + '_' + str(order_id) + '_' + str(id))
            if not os.path.exists(BASE_DIR):
                os.makedirs(BASE_DIR)
            if not os.path.exists(path_folder):
                os.makedirs(path_folder)
            filepath = []
            for f in files:
                path = os.path.join(path_folder, f.name)
                with open(path, 'wb+') as fin:
                    for chunk in f.chunks():
                        fin.write(chunk)
                filepath.append(path)
            if len(filepath) > 0:
                MasterOrder.objects.filter(id=id).update(order_id=order_id, customer=customer, uni=uni, major=major,
                                                         remark=remark, user_id=user_id, filepath=str(filepath))
            else:
                MasterOrder.objects.filter(id=id).update(order_id=order_id, customer=customer, uni=uni, major=major,
                                                         remark=remark, user_id=user_id)
            return JsonResponse({'code': 200, 'msg': 'success', 'master_id': id})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': str(e)})

    def put(self, request):
        # query_dict = request.POST
        master_dict = json.loads(request.body)
        print(master_dict)

        MasterOrder.objects.filter(id=master_dict.get('id')).update(order_id=master_dict.get('orderid'),
                                                                    customer=master_dict.get('customer'),
                                                                    uni=master_dict.get('uni'),
                                                                    major=master_dict.get('major'),
                                                                    remark=master_dict.get('remark'), )
        # master_dict = QueryDict(request.body)
        # for i, item in enumerate(master_dict.items()):
        #     master_dict = eval(item[0])
        #     break
        # print(master_dict.get('orderid'))

        return JsonResponse({'code': 200, 'msg': '修改成功'})


def isStartWithHttp(s):
    if len(s.strip(' ')) > 0 and not s.strip(' ').startswith('http'):
        return 'http://' + s.strip(' ')
    else:
        return s.strip(' ')



class CreateSubOrderView(View):
    """创建子订单"""

    def post(self, request):
        try:
            json_dict = json.loads(request.body)
            print(json_dict)

            if json_dict.get('id', 0):
                master_order_id = json_dict['id']
                print(master_order_id)
                sub_order_list = [json_dict]
            else:
                sub_order_list = json_dict['subOrderList']
                master_order_id = json_dict['masterId']
            sub = []
            for sub_order in sub_order_list:
                writer_id = ''
                writer_name = ''
                if sub_order.get('writer', '') != '':
                    writer_id = sub_order['writer'].split('-')[0]
                    writer_name = re.sub(str(writer_id) + '-', '', sub_order['writer'], count=1)
                if writer_id:
                    status = 1
                else:
                    # 未分配写手
                    status = 6
                sub.append(SubOrder(master_order_id=master_order_id, order_id='', uni=sub_order.get('uni', ''),

                                    major=sub_order.get('major', ''), major_url=isStartWithHttp(sub_order.get('majorurl', '')),
                                    writer_id=writer_id,
                                    writer_name=writer_name, plan=sub_order.get('plan', ''),
                                    course1=sub_order.get('course1',''),
                                    course1_url=isStartWithHttp(sub_order.get('courseurl1', '')), course2=sub_order.get('course2', ''),
                                    course2_url=isStartWithHttp(sub_order.get('courseurl2', '')), course3=sub_order.get('course3', ''),
                                    course3_url=isStartWithHttp(sub_order.get('courseurl3', '')), status=status, writer_status=1,
                                    start_time=UTC2BJS(sub_order.get('time')[0]), end_time=UTC2BJS(sub_order.get('time')[1])))
            SubOrder.objects.bulk_create(sub)
            return JsonResponse({'code': 200, 'msg': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'msg': str(e)})

    def put(self, request):
        sub_dict = json.loads(request.body)
        print(sub_dict)
        order_id = sub_dict.get('orderid')
        uni = sub_dict.get('uni')
        major = sub_dict.get('major')
        major_url = isStartWithHttp(sub_dict.get('major_url'))

        plan = sub_dict.get('plan')
        course1 = sub_dict.get('course1')
        course1_url = isStartWithHttp(sub_dict.get('courseurl1'))
        course2 = sub_dict.get('course2')
        course2_url = isStartWithHttp(sub_dict.get('courseurl2'))
        course3 = sub_dict.get('course3')
        course3_url = isStartWithHttp(sub_dict.get('courseurl3'))
        start_time = sub_dict.get('time')[0]
        end_time = sub_dict.get('time')[1]
        writer_id = sub_dict.get('writer_id')
        writer_name = sub_dict.get('writer_name')
        writer = sub_dict.get('writer')
        if len(writer.split('-')) > 1 and writer[0].isdigit():
            writer_id = writer.split('-')[0]
            writer_name = re.sub(str(writer_id) + '-', '', writer, count=1)

        SubOrder.objects.filter(id=sub_dict.get('id')).update(uni=uni, major=major,
                                                              major_url=major_url,
                                                              writer_id=writer_id, writer_name=writer_name, plan=plan,
                                                              course1=course1, course1_url=course1_url, course2=course2,
                                                              course2_url=course2_url,
                                                              course3=course3, course3_url=course3_url,
                                                              start_time=start_time, end_time=end_time)
        return JsonResponse({'code': 200, 'msg': '修改成功'})


def file_iterator(file, chunk_size=512):
    with open(file, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


# class DownLoadFileView(View):
#     def post(self, request):
#         # path = request.POST.get('path')
#         path = '/home/ld/project/ordermanagement/ordermanagement/statics/qide_undefined_3/cv_template_17feb_1800 (1).docx'
#         print('path:', path)
#         filename = path.split('/')[-1]
#         response = StreamingHttpResponse(file_iterator(path))
#         response['Content-Type'] = 'application/octet-stream'
#         response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
#         return response


class DownLoadFileView(View):
    def post(self, request):
        if request.POST.get('id'):
            id = request.POST.get('id')
            master_order = MasterOrder.objects.filter(id=id)[0]

            filename = str(master_order.customer) + '_' + str(master_order.order_id) + '_' + str(master_order.uni) + '_' + str(
                master_order.major) + '.docx'

            sub_order_list = SubOrder.objects.filter(master_order_id=id)
            document = docx.Document()
            for sub_order in sub_order_list:
                document.add_paragraph(sub_order.text)
            BASE_DIR = os.path.join(Path(__file__).resolve().parent.parent.parent.parent, 'statics')
            if not os.path.exists(BASE_DIR):
                print(BASE_DIR)
                os.makedirs(BASE_DIR)
            path_folder = os.path.join(BASE_DIR,
                                       str(master_order.customer) + '_' + str(master_order.order_id) + '_' + str(
                                           master_order.id))
            if not os.path.exists(path_folder):
                print(path_folder)
                os.makedirs(path_folder)
            path = os.path.join(path_folder, filename)
            document.save(path)
            # return 1
        else:
            path = request.POST.get('path')
        filename = path.split('/')[-1]
        response = StreamingHttpResponse(file_iterator(path))
        response['Content-Type'] = 'application/octet-stream'
        response['Access-Control-Expose-Headers'] = "Content-Disposition, Content-Type"
        response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(filename))
        # response['Content-Disposition'] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(filename))
        return response


class GetOrderView(View):
    # status 状态码
    # status_ 状态码对应的状态
    # status__ 前端用来显示文本颜色，7用来判断deadline超时
    def post(self, request):
        admin = request.POST.get('admin')
        data = []
        userid = request.POST.get('userid')
        if str(admin) == '1':
            master_order_list = MasterOrder.objects.all()
        else:
            master_order_list = MasterOrder.objects.filter(user_id=userid)
        status_list = ["notstarted", "ongoing", "finish", "rejected", "Checking", "unassigned"]
        now = datetime.datetime.now().astimezone()
        for master_order in master_order_list:
            master_done = 1
            master_not_start = 0
            master_start = 0
            filepath = master_order.filepath
            if filepath == '':
                filepath = []
            else:
                filepath = eval(filepath)
            m_order = {'id': master_order.id, 'orderid': master_order.order_id, 'customer': master_order.customer,
                       'user_id': master_order.user_id, 'uni': master_order.uni, 'major': master_order.major,
                       'remark': master_order.remark, 'ismaster': 1, 'children': [], 'status': master_order.status,
                       'status_': status_list[master_order.status - 1], 'filepath': filepath}
            sub_order_list = SubOrder.objects.filter(master_order_id=master_order.id)
            deadline = []
            num_child_done = 0
            for sub_order in sub_order_list:
                # now = datetime.datetime.now().astimezone()
                start_time = sub_order.start_time.astimezone()
                end_time = sub_order.end_time.astimezone()
                # print('ss:', start_time.strftime('%Y-%m-%d %H:%M:%S'))
                status = sub_order.status
                status__ = status
                deadline.append(end_time)
                if status == 3:
                    status = 3
                    num_child_done += 1
                elif status == 4:
                    status = 4
                elif status == 5:
                    status = 5
                elif not sub_order.writer_id:
                    status = 6
                elif now < start_time:
                    status = 1
                elif start_time <= now:
                    status = 2
                if now > end_time:
                    status__ = 7
                # 所有子订单都完成，主订单才是完成状态
                if status != 3:
                    master_done = 0
                # # 如果存在子订单不是 未开始或未分配状态，则把主订单设为进行中
                # if status == 1 or status ==6:
                #     pass
                # else:
                #     master_not_start = 1
                # 如果子订单开始时间小于当前时间，则主订单状态至少为进行中
                if start_time <= now:
                    master_start = 1

                m_order['children'].append({'id': sub_order.id, 'orderid': sub_order.uni + '-' + sub_order.major, 'uni': sub_order.uni,
                                            'major': sub_order.major, 'major_url': sub_order.major_url,
                                            'writer_id': sub_order.writer_id,
                                            'writer': sub_order.writer_name, 'writer_name': sub_order.writer_name,
                                            'course1': sub_order.course1, 'courseurl1': sub_order.course1_url,
                                            'course2': sub_order.course2, 'courseurl2': sub_order.course2_url,
                                            'course3': sub_order.course3, 'courseurl3': sub_order.course3_url,
                                            'plan': sub_order.plan, 'time': [sub_order.start_time, sub_order.end_time],
                                            'ismaster': 0, 'status': status, 'status__': status__,
                                            'deadline': end_time.strftime('%Y-%m-%d %H:%M:%S'), 'text': sub_order.text,
                                            'writerStatus': sub_order.writer_status, 'status_': status_list[status - 1],
                                            'text_comment': sub_order.text_comment
                                            })

            m_order['num_child'] = len(m_order['children'])
            m_order['num_child_done'] = num_child_done
            if deadline:
                print('min:', min(deadline))
                status__ = master_order.status
                if now > min(deadline):
                    status__ = 7
                # if master_not_start:
                if master_start:
                    m_order['status'] = 2
                    m_order['status_'] = status_list[1]
                if master_done:
                    status__ = 3
                    m_order['status'] = 3
                    m_order['status_'] = status_list[2]
                m_order['deadline'] = min(deadline).strftime('%Y-%m-%d %H:%M:%S')
                m_order['status__'] = status__


            data.append(m_order)
        return JsonResponse({'code': 200, 'orderList': data})


class AssignWriterView(View):
    def post(self, request):
        try:
            ismaster = request.POST.get('ismaster')
            print(ismaster)
            id = request.POST.get('id')
            writer_name = request.POST.get('writer')
            writer_id = writer_name.split('-')[0]
            writer_name = re.sub(str(writer_id) + '-', '', writer_name, count=1)
            print(writer_id, writer_name)
            if str(ismaster) == '1':
                print(2)
                sub_order_list = SubOrder.objects.filter(master_order_id=id)
                for sub_order in sub_order_list:
                    if not sub_order.writer_id:
                        sub_order.writer_id = writer_id
                        sub_order.writer_name = writer_name
                        if sub_order.status == 6:
                            sub_order.status = 1
                SubOrder.objects.bulk_update(sub_order_list, ['writer_id', 'writer_name', 'status'])
            else:
                sub_order_list = SubOrder.objects.filter(id=id)
                for sub_order in sub_order_list:
                    sub_order.writer_id = writer_id
                    sub_order.writer_name = writer_name
                    if sub_order.status == 6:
                        sub_order.status = 1
                SubOrder.objects.bulk_update(sub_order_list, ['writer_id', 'writer_name', 'status'])
            return JsonResponse({'code': 200, 'msg': '分配写手成功'})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': str(e)})
