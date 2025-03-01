from django.shortcuts import render
from .models import News

def news_list(request):
    newss = News.objects.all().order_by('-date')
    return render(request, 'news_list.html', {'newss': newss})

