from django.shortcuts import render
from django.http import HttpResponse
from django import forms


def index(request):
    return render(request, 'index.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def detail(request, employer_id):
    return HttpResponse("You're looking at employer %s. " % employer_id)


def results(request, employer_id):
    response = "You're looking at the results of employer %s."
    return HttpResponse(response % employer_id)


def comment(request, employer_id):
    return HttpResponse("You're commenting on employer %s." % employer_id)