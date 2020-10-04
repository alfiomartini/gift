from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import getGitUser, getUserRepos

# Create your views here.


def index(request):
    return HttpResponse('Hello Gift!')


def github_user(request, username):
    user_resp = getGitUser(username)
    # print(resp)
    if 'message' in user_resp:
        return JsonResponse({'error': 'User not found'})
    if 'error' in user_resp:
        return JsonResponse({'error': user_resp['error']})
    repos_resp = getUserRepos(username)
    if 'message' in user_resp:
        return JsonResponse({'error': 'User not found'})
    if 'error' in user_resp:
        return JsonResponse({'error': user_resp['error']})
    user_github = {}
    user_github['user'] = user_resp
    user_github['repos'] = repos_resp
    return JsonResponse(user_github)
