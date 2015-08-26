from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from form import models
from django.template.context_processors import csrf
import os, datetime,json
from form import forms



def home(request):
	print request.method
	if request.method == 'POST':
		# print request.POST
		# print request.FILES
		if request.POST.get("fullName"):
			form = forms.ApplicationForm(request.POST, request.FILES)
			if form.is_valid():
				outCome = form.save()
				return HttpResponse("it worked")
			return HttpResponse(form.errors.as_json(),content_type='application/json',status="400",reason="application didn't work")
		elif request.FILES:
			form = forms.UploadForm(request.POST, request.FILES)
			if form.is_valid():
				outCome = form.save()
				return HttpResponse(outCome.pk)
			return HttpResponse(form.errors.as_json(),content_type='application/json',status="400",reason="something wrong with the form")
		else :
			return HttpResponse(json.dumps({"error":"need to submit something"}),content_type='application/json',status="400",reason="you need to submit something")
		
	form = forms.ApplicationForm()
	return render(request, 'regform.html', { "form":form })

def success(request):
	return HttpResponse("it worked")
