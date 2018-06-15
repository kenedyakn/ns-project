from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from excel_parsers.employer_status_masaka import *
from excel_parsers.ecollection_reporting import *
import xlrd


def index(request):
    return render(request, 'index.html')


def upload_file(request):
    if request.method == 'POST':
        # file = request.FILES['file']
        # print("File name {}".format(file.name))  # Gives name
        handle_uploaded_file(request.FILES['file'])
        return HttpResponseRedirect('/ecollections/')


def handle_uploaded_file(f):
    with open('excel_data/upload.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    db_dump()


def db_dump():
    wbook = xlrd.open_workbook('excel_data/upload.xlsx')
    process_workbook(wbook)


def upload_file_collections(request):
    if request.method == 'POST':
        # file = request.FILES['file']
        # print("File name {}".format(file.name))  # Gives name
        handle_uploaded_file_collections(request.FILES['file_collections'])
        return HttpResponseRedirect('/ecollections/')


def handle_uploaded_file_collections(f):
    with open('excel_data/collections.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        db_dump_collections()


def db_dump_collections():
    wbook = xlrd.open_workbook('excel_data/collections.xlsx')
    process_collections_workbook(wbook)


def detail(request, employer_id):
    return HttpResponse("You're looking at employer %s. " % employer_id)


def results(request, employer_id):
    response = "You're looking at the results of employer %s."
    return HttpResponse(response % employer_id)


def comment(request, employer_id):
    return HttpResponse("You're commenting on employer %s." % employer_id)
