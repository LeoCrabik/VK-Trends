from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
import trendsfinder.text_analizer as Analizer

def index(request):
    if request.method == 'GET':
        return render(request=request, template_name='vktrends/index.html')
    if request.method == 'POST':
        group_id = request.POST.get('group_name')
        group_id = group_id.split('/')[-1]

        import requests
        res = requests.get('https://vk.com/{}'.format(group_id))
        if res.status_code == 404:
            print('Ошибка')
            raise Http404()

        try:
            data = Analizer.get_trends(domain=group_id)
        except:
            return render(request=request, template_name='vktrends/index.html')

        content = {
            'data': data,
            'group_name': group_id,
        }
        return render(request=request, template_name='vktrends/trends.html', context=content)


def page_not_found(request, exception):
    return render(request=request, template_name='vktrends/error404.html')
