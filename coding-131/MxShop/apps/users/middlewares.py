#!/usr/bin/env python
# encoding: utf-8
from django import http
import redis
from users.models import CourseUser
REDIS = {
    "host":"127.0.0.1",
    "port":6379,
}

redis_conn = redis.StrictRedis(host=REDIS["host"], port=REDIS["port"], db=0, charset="utf-8", decode_responses=True)


class FilterUidMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # 调用 view 之前的代码

        ip_addr = request.META['REMOTE_ADDR']
        imooc_uid = request.META.get('HTTP_IMOOC', '')
        if imooc_uid:
            user_courses = CourseUser.objects.using('userbuy').filter(user_uid=imooc_uid, course_id="131")
            if user_courses:
                redis_conn.sadd("imooc_uid_{}".format(imooc_uid), ip_addr)
                if redis_conn.scard("imooc_uid_{}".format(imooc_uid)) > 4:
                    return http.HttpResponseForbidden('<h1>Forbidden</h1>')
                response = self.get_response(request)
                return response
            else:
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        else:
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')


    # def process_request(self, request):
    #     ip_addr = request.META['REMOTE_ADDR']
    #     imooc_uid = request.META.get('IMOOC_UID', '')
    #     if imooc_uid:
    #         user_courses = CourseUser.objects.using('userbuy').filter(user_uid=imooc_uid, course_id="131")
    #         if user_courses:
    #             redis_conn.sadd("imooc_uid_{}".format(imooc_uid), ip_addr)
    #             if redis_conn.scard("imooc_uid_{}".format(imooc_uid)) > 4:
    #                 return http.HttpResponseForbidden('<h1>Forbidden</h1>')
    #             else:
    #                 return  None
    #         else:
    #             return http.HttpResponseForbidden('<h1>Forbidden</h1>')
    #     else:
    #         return http.HttpResponseForbidden('<h1>Forbidden</h1>')