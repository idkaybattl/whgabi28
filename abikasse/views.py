from django.http import HttpResponse
from django.template import loader


def abikasse(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
