from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import getGitUser, getUserRepos, formatRep
from .utils import getUsers, getRepos, buildPaging
from .models import GitRequest
import json

# Create your views here.


def index(request):
    api_requests = GitRequest.objects.all()
    # print('api requests', api_requests)
    return render(request, 'gift/index.html', {})


def user_render(request, username):
    current_page = int(request.GET.get('page', 1))
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
        json_resp, repos_resp = getUserRepos(username, current_page)
        # print('repos_resp', repos_resp)
        # print('resp links', json_resp.links)
        links = json_resp.links
        paging = buildPaging(links, current_page)
        # print('paging', paging)
        repos_resp = formatRep(repos_resp)
        # for rep in repos_resp:
        #     print(rep['name'], rep['created_at'])
        # repos_resp.sort(key=lambda x: x['created_at'], reverse=True)
        # print('')
        # for rep in repos_resp:
        #     print(rep['name'], rep['created_at'])
        GitRequest.objects.create(request_text=request_text, req_type='user')
        context = {'user': user_resp, 'repos': repos_resp, 'paging': paging}
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
    current_page = int(request.GET.get('page', 1))
    place, sep, username = query.partition(':')
    # remove trailing or leading spaces
    place_ = place.strip()
    username_ = username.strip()
    request_text = place_ + sep + username_
    json_resp, users_resp = getUsers(username_, place_, current_page)
    # print('users resp', users_resp)
    if users_resp['total_count'] > 0:
        links = json_resp.links
        paging = buildPaging(links, current_page)
        # print('paging', paging)
        GitRequest.objects.create(request_text=request_text, req_type=place_)
        return render(request, 'gift/users.html', {'users': users_resp,
                                                   'paging': paging})
    else:
        return render(request, 'gift/error.html',
                      {'message': 'Sorry. No users found.'})


def search_repos(request, query):
    current_page = int(request.GET.get('page', 1))
    place, sep, reponame = query.partition(':')
    # remove trailing or leading spaces
    place_ = place.strip()
    reponame_ = reponame.strip()
    request_text = place_ + sep + reponame_
    json_resp, repos_resp = getRepos(reponame_, place_, current_page)
    if repos_resp['total_count'] > 0:
        # print('resp headesr', json_resp.headers)
        # print('resp links', json_resp.links)
        links = json_resp.links
        paging = buildPaging(links, current_page)
        # print('paging', paging)
        GitRequest.objects.create(request_text=request_text, req_type=place_)
        # return JsonResponse(repos_resp)
        return render(request, 'gift/repos.html', {'repos': repos_resp,
                                                   'paging': paging})
    else:
        return render(request, 'gift/error.html',
                      {'message': 'Sorry. No repositories found.'})


# this should be useful as an ajax request


def user_repos(request, username):
    current_page = int(request.GET.get('page', 1))
    if username.startswith('user:'):
        prefix, separator, username = username.partition(':')
        username = username.strip()
        request_text = prefix + separator + username
    else:
        request_text = 'user:' + username
    json_resp, repos_resp = getUserRepos(username, current_page)
    links = json_resp.links
    paging = buildPaging(links, current_page)
    # print('paging', paging)
    repos_resp = formatRep(repos_resp)
    repos_resp.sort(key=lambda x: x['created_at'], reverse=True)
    GitRequest.objects.create(request_text=request_text, req_type='user')
    context = {'repos': repos_resp, 'paging': paging}
    return render(request, 'gift/user_repos.html', context=context)


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
