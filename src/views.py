from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic


def index(request: HttpRequest):
    print(type(request.user.id))
    return HttpResponse(request.user.id)
