from django.shortcuts import render
import time
import json
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .test import test
from .classifier.text_classifier import nb_classifier


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(None, request))


def classify(request):
    start = time.time()
    email = request.POST["data"]
    print(email)
    a = nb_classifier(email)
    print(a)
    data = {
        "normal": round(a, 5) * 100,
        "spam": round(1 - a, 5) * 100,
        "data": email
    }
    end = time.time()
    data["time"] = round((end - start) * 1000, 5)
    return HttpResponse(json.dumps(data), content_type="application/json")
