from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import getGitUser, getUserRepos, formatRep
from .utils import getUsers, getRepos
from .models import GitRequest

# Create your views here.


def index(request):
    api_requests = GitRequest.objects.all()
    print('api requests', api_requests)
    return render(request, 'gift/layout.html', {})


def user_render(request, username):
    if username.startswith('user:'):
        prefix, separator, username = username.partition(':')
        username = username.strip()
        request_text = prefix + separator + username
    else:
        request_text = 'user:' + username
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
        GitRequest.objects.create(request_text=request_text, req_type='user')
        context = {'user': user_resp, 'repos': repos_resp}
        return render(request, 'gift/user.html', context=context)


def user_post(request):
    if request.method == 'POST':
        # get username from form and remove spaces from
        # both ends
        username = request.POST['username'].strip()
        if username.startswith('name:') or username.startswith('login:'):
            return redirect('search_users', query=username)
        elif username.startswith('repo:') or username.startswith('readme') or username.startswith('description'):
            return redirect('search_repos', query=username)
        elif username.startswith('user:'):
            return redirect('user_render', username=username)
        else:
            return redirect('user_render', username=username)


def search_users(request, query):
    place, sep, username = query.partition(':')
    # remove trailing or leading spaces
    place_ = place.strip()
    username_ = username.strip()
    request_text = place_ + sep + username_
    users_resp = getUsers(username_, place_)
    GitRequest.objects.create(request_text=request_text, req_type=place_)
    return render(request, 'gift/users.html', {'users': users_resp})


def search_repos(request, query):
    place, sep, reponame = query.partition(':')
    # remove trailing or leading spaces
    place_ = place.strip()
    reponame_ = reponame.strip()
    request_text = place_ + sep + reponame_
    repos_resp = getRepos(reponame_, place_)
    GitRequest.objects.create(request_text=request_text, req_type=place_)
    # return JsonResponse(repos_resp)
    return render(request, 'gift/repos.html', {'repos': repos_resp})

# this should be useful as an ajax request


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
