from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    if request.method == 'GET':
        return render(request=request, template_name='vktrends/index.html')
    if request.method == 'POST':
        print('POST POST POST')
        group_id = request.POST.get('group_name')
        print(request)
        return HttpResponseRedirect('/{}'.format(group_id))


def group(request, groupid):
    import requests
    res = requests.get('https://vk.com/{}'.format(groupid))
    print(res.status_code)
    if res.status_code == 404:
        print('Ошибка')
        raise Http404()
    content = {
        'group_name': groupid
    }
    return render(request=request, template_name='vktrends/group.html', context=content)


def page_not_found(request, exception):
    return render(request=request, template_name='vktrends/error404.html')
