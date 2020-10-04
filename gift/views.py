from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import getGitUser, getUserRepos

# Create your views here.


def index(request):
    return render(request, 'gift/layout.html', {})


def github_post(request):
    if request.method == 'POST':
        # get username from form and remove spaces from
        # both ends
        username = request.POST['username'].strip()
        user_resp = getGitUser(username)
        if 'message' in user_resp:
            return render(request, 'gift/error.html',
                          {'message': 'User not found'})
        elif 'error' in user_resp:
            return render(request, 'gift/error.html',
                          {'message': user_resp['error']})
        else:
            repos_resp = getUserRepos(username)
            return render(request, 'gift/github.html', {'user': user_resp, 'repos': repos_resp})


def github_get(request, username):
    user_resp = getGitUser(username)
    if 'message' in user_resp:
        return JsonResponse({'error': 'User not found'})
    elif 'error' in user_resp:
        return JsonResponse({'error': user_resp['error']})
    else:
        repos_resp = getUserRepos(username)
        return JsonResponse({'user': user_resp, 'repos': repos_resp})
