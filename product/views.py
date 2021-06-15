from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
import json

from .models import (
    Subject,
) 
# Create your views here.


# Download counter
def download_counter(request):
    Subject.objects.filter(slug = request.GET.get('request_data')).update(downloaded = F('downloaded')+1)
    return HttpResponse(
        json.dumps('Increased'),
        content_type="application/json"
    )