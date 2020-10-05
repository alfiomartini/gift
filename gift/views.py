from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import getGitUser, getUserRepos
from datetime import datetime

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
        #  maps date iso strings into datetime objects
        # see: https://stackabuse.com/converting-strings-to-datetime-in-python/
        for rep in repos_resp:
            created_str = rep['created_at'].replace('T', ' ')
            created_str = created_str.replace('Z', '')
            created_at = datetime.strptime(
                created_str, "%Y-%m-%d %H:%M:%S")
            rep['created_at'] = created_at

            updated_str = rep['updated_at'].replace('T', ' ')
            updated_str = updated_str.replace('Z', '')
            updated_at = datetime.strptime(
                updated_str, "%Y-%m-%d %H:%M:%S")
            rep['updated_at'] = updated_at

            cropped_name = rep['name'][0:15]
            new_name = cropped_name + ' '
            rep['name'] = new_name
        repos_resp.sort(key=lambda x: x['created_at'], reverse=True)
        context = {'user': user_resp, 'repos': repos_resp}
        return render(request, 'gift/github.html', context=context)


def user_post(request):
    if request.method == 'POST':
        # get username from form and remove spaces from
        # both ends
        username = request.POST['username'].strip()
        return redirect('user_render', username=username)


def user_get(request, username):
    user_resp = getGitUser(username)
    if 'message' in user_resp:
        return JsonResponse({'error': 'User not found'})
    elif 'error' in user_resp:
        return JsonResponse({'error': user_resp['error']})
    else:
        repos_resp = getUserRepos(username)
        for rep in repos_resp:
            created_str = rep['created_at'].replace('T', ' ')
            created_str = created_str.replace('Z', '')
            created_at = datetime.strptime(
                created_str, "%Y-%m-%d %H:%M:%S")
            rep['created_at'] = created_at

            updated_str = rep['updated_at'].replace('T', ' ')
            updated_str = updated_str.replace('Z', '')
            updated_at = datetime.strptime(
                updated_str, "%Y-%m-%d %H:%M:%S")
            rep['updated_at'] = updated_at

            cropped_name = rep['name'][0:15]
            new_name = cropped_name + ' '
            rep['name'] = new_name
        repos_resp.sort(key=lambda x: x['created_at'], reverse=True)
        return JsonResponse({'user': user_resp, 'repos': repos_resp})
