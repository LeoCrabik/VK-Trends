from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from trendsfinder.text_analizer import TopicsFinder


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
            topics = TopicsFinder(domain=group_id)
            content = topics.get_content()
            # print(content)

            return render(request=request, template_name='vktrends/trends.html', context=content)
        except Exception as e:
            raise Http404()

def page_not_found(request, exception):
    return render(request=request, template_name='vktrends/error404.html')
