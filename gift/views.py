from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import getGitUser, getUserRepos, formatRep
from .utils import getUsers, getRepos, buildPaging
from .models import GitRequest
from datetime import datetime, timedelta
from dateutil import tz
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
import json

# Create your views here.


def index(request):
    # api_requests = GitRequest.objects.all()
    # # print(api_requests)
    # num_requests = GitRequest.objects.all().count()
    # user_searches = GitRequest.objects.filter(req_type='user').count()
    # print('user searches', user_searches)
    # users_name = GitRequest.objects.filter(req_type='name').count()
    # print('users name', users_name)
    # users_login = GitRequest.objects.filter(req_type='login').count()
    # print('users login', users_login)
    # reps_name = GitRequest.objects.filter(req_type='repo').count()
    # print('reps name', reps_name)
    # reps_readme = GitRequest.objects.filter(req_type='readme').count()
    # print('reps readme', reps_readme)
    # reps_desc = GitRequest.objects.filter(req_type='desc').count()
    # print('reps desc', reps_desc)
    # sum_cats = user_searches + users_name + \
    #     users_login + reps_name + reps_readme + reps_desc
    # print('num requests', num_requests)
    # print('sum by cats', sum_cats)
    # yesterday = datetime.now(tz=tz.tzlocal()) + timedelta(days=-1)
    # sixhours = datetime.now(tz=tz.tzlocal()) + timedelta(hours=-6)
    # twohours = datetime.now(tz=tz.tzlocal()) + timedelta(hours=-2)
    # print('yesterday', yesterday)
    # print('sixhours', sixhours)
    # req_yesterday = GitRequest.objects.filter(date__gte=yesterday)
    # req_sixhours = GitRequest.objects.filter(date__gte=sixhours)
    # req_twohours = GitRequest.objects.filter(date__gte=twohours)
    # print('all requests', api_requests.count())
    # print('last 24 hours', req_yesterday.count())
    # print('last sixhours', req_sixhours.count())
    # print('last twohours', req_twohours.count())
    return render(request, 'gift/index.html', {})


def readme(request):
    return render(request, 'gift/readme.html', {})


def user_render(request, username):
    current_page = int(request.GET.get('page', 1))
    if username.startswith('user:'):
        prefix, separator, username = username.partition(':')
        username = username.strip()
        request_text = prefix + separator + username
    else:
        request_text = 'user:' + username
    user_resp = getGitUser(username)
    # If user is not found, try users:
    if 'message' in user_resp:
        return redirect('search_users', query='name:' + username)
        # return render(request, 'gift/error.html',
        #               {'message': 'User not found'})
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
        # not needed anymore
        # for rep in repos_resp:
        #     print(rep['name'], rep['created_at'])
        # repos_resp.sort(key=lambda x: x['created_at'], reverse=True)
        # print('')
        # for rep in repos_resp:
        #     print(rep['name'], rep['created_at'])
        GitRequest.objects.create(request_text=request_text, req_type='user')
        context = {'user': user_resp, 'repos': repos_resp, 'paging': paging}
        return render(request, 'gift/user.html', context=context)


# @ensure_csrf_cookie
def user_post(request):
    if request.method == 'POST':
        # get username from form and remove spaces from
        # both ends
        username = request.POST['username'].strip()
        print(f'Hello {username}')
        if username.startswith('name:') or username.startswith('login:'):
            return redirect('search_users', query=username)
        elif username.startswith('repo:') or username.startswith('readme') or username.startswith('desc:'):
            return redirect('search_repos', query=username)
        elif username.startswith('user:'):
            return redirect('user_render', username=username)
        else:
            return redirect('user_render', username=username)
    else:
        print('error?')


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


# these are used by ajax requests:

def charts(request, category):
    chart = {}
    chart['labels'] = ['user', 'name', 'login', 'repo', 'readme', 'desc']
    if category == 'total':
        everything = GitRequest.objects.all().count()
        user = GitRequest.objects.filter(req_type='user').count()
        name = GitRequest.objects.filter(req_type='name').count()
        login = GitRequest.objects.filter(req_type='login').count()
        repo = GitRequest.objects.filter(req_type='repo').count()
        readme = GitRequest.objects.filter(req_type='readme').count()
        desc = GitRequest.objects.filter(req_type='desc').count()
        chart['all'] = everything
        chart['label'] = f'{everything} searches - all'
        chart['data'] = [user, name, login, repo, readme, desc]
    elif category == '7days':
        sevendays = datetime.now(tz=tz.tzlocal()) + timedelta(days=-7)
        everything = GitRequest.objects.filter(date__gte=sevendays).count()
        user = GitRequest.objects.filter(
            req_type='user', date__gte=sevendays).count()
        name = GitRequest.objects.filter(
            req_type='name', date__gte=sevendays).count()
        login = GitRequest.objects.filter(
            req_type='login', date__gte=sevendays).count()
        repo = GitRequest.objects.filter(
            req_type='repo', date__gte=sevendays).count()
        readme = GitRequest.objects.filter(
            req_type='readme', date__gte=sevendays).count()
        desc = GitRequest.objects.filter(
            req_type='desc', date__gte=sevendays).count()
        chart['all'] = everything
        chart['label'] = f'{everything} searches - 7 days'
        chart['data'] = [user, name, login, repo, readme, desc]
    elif category == '1day':
        yesterday = datetime.now(tz=tz.tzlocal()) + timedelta(days=-1)
        everything = GitRequest.objects.filter(date__gte=yesterday).count()
        user = GitRequest.objects.filter(
            req_type='user', date__gte=yesterday).count()
        name = GitRequest.objects.filter(
            req_type='name', date__gte=yesterday).count()
        login = GitRequest.objects.filter(
            req_type='login', date__gte=yesterday).count()
        repo = GitRequest.objects.filter(
            req_type='repo', date__gte=yesterday).count()
        readme = GitRequest.objects.filter(
            req_type='readme', date__gte=yesterday).count()
        desc = GitRequest.objects.filter(
            req_type='desc', date__gte=yesterday).count()
        chart['all'] = everything
        chart['label'] = f'{everything} searches - 24h'
        chart['data'] = [user, name, login, repo, readme, desc]
    return JsonResponse(chart)


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
