from django.http import HttpResponse
from django.template import	Context
from django.shortcuts import render_to_response

def index(request):
	context = Context({"my_name": "Adrian"})
	return render_to_response("index.html", context)