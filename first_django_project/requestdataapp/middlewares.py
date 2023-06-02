import time

from django.http import HttpRequest
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):
    print("initial call")
    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self,get_response):
         self.get_response = get_response
         self.request_count = 0
         self.request_time = {}
         self.responses_count = 0
         self.exceptions_count = 0


    def __call__(self,request: HttpRequest):
        time_delay = 10 # min delta between requests
        if not self.request_time:
            print('This is the first request of this user after server was restarted')
        else:
            if (round(time.time()) * 1) - self.request_time['time'] < time_delay \
                    and self.request_time['ip_address'] == request.META.get('REMOTE_ADDR'):
                print('It has been less than 10 seconds since the last request from your ip address')
                return render(request, 'requestdataapp/error-request.html')
        self.request_time = {'time': round(time.time()) * 1, 'ip-address': request.META.get('REMOTE_ADDR')}

        self.request_count += 1
        print("request count", self.request_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")



