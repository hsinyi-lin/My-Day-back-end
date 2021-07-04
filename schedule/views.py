from django.shortcuts import render
# rest
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
# my day
from schedule.serializers import ScheduleSerilizer
from api.models import Schedule, ScheduleNotice, PersonalSchedule, Account, Type, GroupMember, Group
# schedule
from schedule.resopnse import *


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerilizer

    # /schedule/create_new/  -------------------------------------------------------------------------------------------
    @action(detail=False, methods=['POST'])
    def create_new(self, request):
        data = request.data

        uid = data.get('uid')
        title = data.get('title')
        start_time = data.get('startTime')
        end_time = data.get('endTime')
        remind = data.get('remind')
        remind_time = remind.get('remindTime')
        is_notice = remind.get('isRemind')
        type_id = data.get('typeId')
        is_countdown = data.get('isCountdown')
        place = data.get('place')
        remark = data.get('remark')

        try:
            new_schedule = Schedule.objects.create(schedule_name=title, type_id=type_id, schedule_start=start_time,
                                                   schedule_end=end_time, place=place)
            new_schedule.save()

            schedule_no = Schedule.objects.get(serial_no=new_schedule.serial_no)

            new_personal_schedule = PersonalSchedule.objects.create(user_id=uid, schedule_no=schedule_no,
                                                                    is_notice=is_notice, is_countdown=is_countdown,
                                                                    is_hidden=False, remark=remark)
            new_personal_schedule.save()
            personal_schedule_no = PersonalSchedule.objects.get(serial_no=new_personal_schedule.serial_no)

            for i in remind_time:
                new_schedule_notice = ScheduleNotice.objects.create(personal_schedule_no=personal_schedule_no,
                                                                    notice_time=i)
                new_schedule_notice.save()
        except:
            return err()

        return success()

    # /schedule/edit/  -------------------------------------------------------------------------------------------------
    @action(detail=False, methods=['POST'])
    def edit(self, request):
        data = request.data

        uid = data.get('uid')
        schedule_no = data.get('scheduleNum')
        try:
            schedule = Schedule.objects.get(serial_no=schedule_no)
        except:
            return schedule_not_found()
        try:
            personal_schedule = PersonalSchedule.objects.get(schedule_no=schedule,
                                                             user=Account.objects.get(user_id=uid))
        except:
            group_member = GroupMember.objects.filter(group_no=schedule.connect_group_no.serial_no, user_id=uid,
                                                      status=1)

            if len(group_member) <= 0:
                group_member = GroupMember.objects.filter(group_no=schedule.connect_group_no.serial_no, user_id=uid,
                                                          status=4)

            if len(group_member) > 0:
                personal_schedule = PersonalSchedule.objects.create(user=Account.objects.get(user_id=uid),
                                                                    schedule_no=schedule, is_notice=False,
                                                                    is_countdown=False, is_hidden=False)
            else:
                return personal_schedule_not_found()

        try:
            schedule_notice = ScheduleNotice.objects.filter(personal_schedule_no=personal_schedule)
            schedule_notice_list = []
            for i in schedule_notice:
                schedule_notice_list.append(str(i.notice_time))
        except:
            schedule_notice_list = []

        title = data.get('title') if data.get('title') != schedule.schedule_name else None
        start_time = data.get('startTime') if data.get('startTime') != schedule.schedule_start else None
        end_time = data.get('endTime') if data.get('endTime') != schedule.schedule_end else None
        remind = data.get('remind')
        is_remind = remind.get('isRemind')
        remind_time = remind.get('remindTime')
        type_id = data.get('typeId') if data.get('typeId') != schedule.type else None
        is_countdown = data.get('isCountdwn') if data.get('isCountdwn') != personal_schedule.is_countdown else None
        place = data.get('place') if data.get('place') != schedule.place else None
        remark = data.get('remark') if data.get('remark') != personal_schedule.remark else None

        def update_remind():
            for i in remind_time:
                if i in schedule_notice_list:
                    continue
                else:
                    ScheduleNotice.objects.create(personal_schedule_no=personal_schedule, notice_time=i)

            for i in schedule_notice_list:
                if i not in remind_time:
                    del_notice = ScheduleNotice.objects.get(personal_schedule_no=personal_schedule, notice_time=i)
                    del_notice.delete()

        if title is not None:
            schedule.schedule_name = title

        if start_time is not None:
            schedule.schedule_start = start_time

        if end_time is not None:
            schedule.schedule_end = end_time

        if remind is not None:
            if is_remind is not None:
                personal_schedule.is_notice = is_remind
            if len(remind_time) > 0:
                update_remind()
        else:
            personal_schedule.is_notice = False

        if type_id is not None:
            schedule.type_id = type_id

        if is_countdown is not None:
            personal_schedule.is_countdown = is_countdown

        if place is not None:
            schedule.place = place

        if remark is not None:
            personal_schedule.remark = remark

        schedule.save()
        personal_schedule.save()

        return success()

    # /schedule/delete/  -----------------------------------------------------------------------------------------------
    @action(detail=False, methods=['POST'])
    def delete(self, request):
        data = request.data

        uid = data.get('uid')
        schedule_no = data.get('scheduleNum')

        try:
            personal_schedule = PersonalSchedule.objects.get(schedule_no=schedule_no, user_id=uid)
            personal_schedule_no = personal_schedule.serial_no
        except:
            return personal_schedule_not_found()

        try:
            schedule_notice = ScheduleNotice.objects.filter(personal_schedule_no=personal_schedule_no)
            schedule_notice.delete()
        except:
            pass

        try:
            personal_schedule.delete()
        except:
            return err()

        return success()

    # /schedule/get/  --------------------------------------------------------------------------------------------------
    @action(detail=False)
    def get(self, request):
        data = request.query_params

        uid = data.get('uid')
        schedule_no = data.get('scheduleNum')

        try:
            schedule = Schedule.objects.get(serial_no=schedule_no)
        except:
            return schedule_not_found()

        try:
            personal_schedule = PersonalSchedule.objects.get(schedule_no=schedule, user=uid)
        except:
            return personal_schedule_not_found()
        try:
            schedule_notice = ScheduleNotice.objects.filter(personal_schedule_no=personal_schedule)
            remind = []
            for i in schedule_notice:
                remind.append(str(i.notice_time))
        except:
            remind = []

        response = {'title': schedule.schedule_name,
                    'startTime': str(schedule.schedule_start),
                    'endTime': str(schedule.schedule_end),
                    'remind': {
                        'isRemind': personal_schedule.is_notice,
                        'remindTime': remind
                    },
                    'typeId': schedule.type_id,
                    'isCountdown': personal_schedule.is_countdown,
                    'place': schedule.place,
                    'remark': personal_schedule.remark}
        return success(response)

    # /schedule/get_list/  ---------------------------------------------------------------------------------------------
    @action(detail=False)
    def get_list(self, request):
        data = request.query_params

        uid = data.get('uid')

        try:
            personal_schedule = PersonalSchedule.objects.filter(user=uid).all()
        except:
            return err()

        if len(personal_schedule) == 0:
            return no_personal_schedule()

        schedule_list = []
        try:
            for i in personal_schedule:
                schedule = Schedule.objects.get(serial_no=i.schedule_no.serial_no)
                schedule_list.append(
                    {
                        'scheduleNum': schedule.serial_no,
                        'title': schedule.schedule_name,
                        'startTime': schedule.schedule_start,
                        'endTime': schedule.schedule_end,
                        'typeId': schedule.type_id
                    }
                )
        except:
            return Response({'response': False,
                             'message': '行程不存在'
                             }, status=status.HTTP_404_NOT_FOUND)

        return Response({'schedule': schedule_list,
                         'response': True,
                         }, status=status.HTTP_200_OK)
    # /schedule/create_common/  -------------------------------------------------------------------------------------------
    # @action(detail=False, methods=['POST'])
    # def create_common(self,request):

    # /schedule/get_common/  -------------------------------------------------------------------------------------------
    # /schedule/common_list/ -------------------------------------------------------------------------------------------
    # /schedule/common_hidden/  ----------------------------------------------------------------------------------------
    # /schedule/countdown_list/  ---------------------------------------------------------------------------------------
