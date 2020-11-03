from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import getGitUser, getUserRepos, formatRep
from .utils import getUsers, getRepos, buildPaging
from .utils import SortRepos, SortUsers, SortUserReps
from .models import GitRequest, AdvSettings
from datetime import datetime, timedelta
from dateutil import tz
# from .adv_search import config
# from .models import config_db
import json

# create sorting menu for repositories, users
sort_repos = SortRepos()
sort_users = SortUsers()
sort_user_reps = SortUserReps()


def index(request):
    # settings = config_db.getConfigAll()
    return render(request, 'gift/index.html', {})


def index_adv(request):
    # print('advanced', config.getConfig('advanced'))
    config_db = AdvSettings.objects.get(id=1)
    settings = config_db.getConfigAll()
    return render(request, 'gift/index_adv.html', {'settings': settings})


def readme(request):
    return render(request, 'gift/readme.html', {})


def user_render(request, username, sort):
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
        return redirect('search_users', query='name:' + username, sort=sort)
    elif 'error' in user_resp:
        return render(request, 'gift/error.html',
                      {'message': user_resp['error']})
    else:  # Let us get the public reps
        direction = 'desc'
        if sort == 'name_asc':
            direction = 'asc'
        sort_user_reps.setThisSort(sort)
        if sort == 'name_asc' or sort == 'name_desc':
            sort = 'full_name'
        menu_list = sort_user_reps.sortUserReps()
        json_resp, repos_resp = getUserRepos(
            username, current_page, sort, direction)
        links = json_resp.links
        paging = buildPaging(links, current_page)
        repos_resp = formatRep(repos_resp)
        GitRequest.objects.create(request_text=request_text, req_type='user')
        context = {'user': user_resp, 'repos': repos_resp,
                   'paging': paging, 'menu_list': menu_list,
                   'query': request_text, 'page': current_page}
        return render(request, 'gift/user.html', context=context)


def user_post(request):
    if request.method == 'POST':
        # get username from form and remove spaces from
        # both ends
        username = request.POST['username'].strip()
        # print(f'Hello {username}')
        if username.startswith('name:') or username.startswith('login:'):
            return redirect('search_users', query=username, sort='best')
        elif username.startswith('repo:') or username.startswith('readme') or username.startswith('desc:'):
            return redirect('search_repos', query=username, sort='stars')
        elif username.startswith('user:'):
            return redirect('user_render', username=username, sort='updated')
        else:
            return redirect('user_render', username=username, sort='updated')
    else:
        print('error?')


def search_users(request, query, sort):
    # print('current sort', sort)
    current_page = int(request.GET.get('page', 1))
    place, sep, username = query.partition(':')
    # remove trailing or leading spaces
    place_ = place.strip()
    username_ = username.strip()
    request_text = place_ + sep + username_
    json_resp, users_resp = getUsers(username_, place_, current_page, sort)
    # print('users resp', users_resp)
    if users_resp['total_count'] > 0:
        sort_users.setThisSort(sort)
        menu_list = sort_users.sortUsers()
        links = json_resp.links
        paging = buildPaging(links, current_page)
        # print('paging', paging)
        GitRequest.objects.create(request_text=request_text, req_type=place_)
        return render(request, 'gift/users.html', {'users': users_resp,
                                                   'paging': paging,
                                                   'menu_list': menu_list,
                                                   'query': request_text,
                                                   'page': current_page})
    else:
        return render(request, 'gift/error.html',
                      {'message': 'Sorry. No users found.'})


def search_repos(request, query, sort):
    # print('current sort', sort)
    current_page = int(request.GET.get('page', 1))
    place, sep, reponame = query.partition(':')
    # remove trailing or leading spaces
    place_ = place.strip()
    reponame_ = reponame.strip()
    request_text = place_ + sep + reponame_
    json_resp, repos_resp = getRepos(
        reponame_, place_, current_page, sort=sort)
    if repos_resp['total_count'] > 0:
        sort_repos.setThisSort(sort)
        menu_list = sort_repos.sortRepos()
        links = json_resp.links
        paging = buildPaging(links, current_page)
        # print('paging', paging)
        GitRequest.objects.create(request_text=request_text, req_type=place_)
        # return JsonResponse(repos_resp)
        return render(request, 'gift/repos.html', {'repos': repos_resp,
                                                   'paging': paging,
                                                   'menu_list': menu_list,
                                                   'query': request_text,
                                                   'page': current_page
                                                   })
    else:
        return render(request, 'gift/error.html',
                      {'message': 'Sorry. No repositories found.'})


# these are used by ajax requests:

def reset_adv(request):
    # print('Hello reset')
    config_db = AdvSettings.objects.get(id=1)
    config_db.init_db()
    return redirect('index_adv')
    # return JsonResponse({'message': 'Config reseted'})


def apply_adv(request):
    if request.method == 'POST':
        config_db = AdvSettings.objects.get(id=1)
        # print('Hello apply_adv')
        # https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
        checked = request.POST.get('adv_check', 'off')
        # print('checked', checked)
        # print('type of checked', type(checked))
        if checked == 'on':
            advanced = True
        else:
            advanced = False
        followers = request.POST['followers']
        forks = request.POST['forks']
        repositories = request.POST['repositories']
        stars = request.POST['stars']
        created_str = request.POST['created']
        print('created', created_str)
        # created = datetime.strptime(created_str, "%Y-%m-%d")
        updated_str = request.POST['updated']
        # updated = datetime.strptime(updated_str, "%Y-%m-%d")
        # print('updated', updated_str)
        config_db.setConfig(advanced=advanced, followers=followers, forks=forks,
                            stars=stars, repositories=repositories,
                            created=created_str, updated=updated_str)
        return redirect('index_adv')


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
