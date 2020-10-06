from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import getGitUser, getUserRepos, formatRep
from .utils import getUsers, getRepos

# Create your views here.


def index(request):
    return render(request, 'gift/layout.html', {})


def user_render(request, username):
    user_resp = getGitUser(username)
    if 'message' in user_resp:
        return render(request, 'gift/error.html',
                      {'message': 'User not found'})
    elif 'error' in user_resp:
        return render(request, 'gift/error.html',
                      {'message': user_resp['error']})
    else:
        repos_resp = getUserRepos(username)
        repos_resp = formatRep(repos_resp)
        repos_resp.sort(key=lambda x: x['created_at'], reverse=True)
        context = {'user': user_resp, 'repos': repos_resp}
        return render(request, 'gift/user.html', context=context)


def user_post(request):
    if request.method == 'POST':
        # get username from form and remove spaces from
        # both ends
        username = request.POST['username'].strip()
        if username.startswith('name:') or username.startswith('login:'):
            return redirect('search_users', query=username)
        elif username.startswith('repo:') or username.startswith('readme') or username.startswith('readme'):
            return redirect('search_repos', query=username)
        else:
            return redirect('user_render', username=username)


def user_get(request, username):
    user_resp = getGitUser(username)
    if 'message' in user_resp:
        return JsonResponse({'error': 'User not found'})
    elif 'error' in user_resp:
        return JsonResponse({'error': user_resp['error']})
    else:
        repos_resp = getUserRepos(username)
        repos_resp = formatRep(repos_resp)
        repos_resp.sort(key=lambda x: x['created_at'], reverse=True)
        return JsonResponse({'user': user_resp, 'repos': repos_resp})


def search_users(request, query):
    place, sep, username = query.partition(':')
    # remove trailing or leading spaces
    place_ = place.strip()
    username_ = username.strip()
    users_resp = getUsers(username_, place_)
    return render(request, 'gift/users.html', {'users': users_resp})


def search_repos(request, query):
    place, sep, reponame = query.partition(':')
    # remove trailing or leading spaces
    place_ = place.strip()
    reponame_ = reponame.strip()
    repos_resp = getRepos(reponame_, place_)
    # return JsonResponse(repos_resp)
    return render(request, 'gift/repos.html', {'repos': repos_resp})
