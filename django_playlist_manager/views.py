from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .spotify import SpotifyCredentials


def index(request: HttpRequest):
    print(type(request.user.id))
    print(SpotifyCredentials(1))
    return HttpResponse(request.user.id)
