from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from excel_parsers.employer_status_masaka import *
from excel_parsers.ecollection_reporting import *
import xlrd

database_username = 'phpmyadmin'
database_password = '123!@#QWEasd'
database_ip = 'localhost'
database_name = 'nssf_db'
employers_table = 'employers'
payments_table = 'payments'
collections_table = 'collections'


def index(request):
    return render(request, 'index.html')


##Handles file upload
def upload_file(request):
    if request.method == 'POST':
        # file = request.FILES['file']
        # print("File name {}".format(file.name))  # Gives name
        if request.FILES:
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'index.html', {"status": "Upload successful"})
        else:
            return render(request, 'index.html', {"status": "No file selected"})


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
        if request.FILES:
            warnings = handle_uploaded_file_collections(request.FILES['file_collections'])
            if warnings["cnop"] == 0 and warnings["cdup"] == 0:
                return render(request, 'index.html', {"status": "Upload successful"})
            else:
                return render(request, 'index.html', {"warnings": warnings, "status": "File uploaded with warnings"})
        else:
            return render(request, 'index.html', {"status": "No file selected"})


def handle_uploaded_file_collections(f):
    with open('excel_data/collections.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return db_dump_collections()


def db_dump_collections():
    wbook = xlrd.open_workbook('excel_data/collections.xlsx')
    value = process_collections_workbook(wbook)
    return value


##Finishes handling file uploads


def get_all_collections(request):
    conn = mysql.connector.connect(user=database_username, password=database_password, host=database_ip,
                                   database=database_name)
    cursor = conn.cursor()
    cursor.execute(
        'select e.employer_number, e.employer_name, p.amount, p.date from employers e '
        'left join payments p on e.employer_number = p.employer_number')
    data_list = cursor.fetchall()
    conn.close()
    return render(request, 'collections.html', {'collections': data_list})


def filter_search(request):
    employer_name = request.GET.get('employer_name')
    employer_number = request.GET.get('employer_number')
    year = request.GET.get('year')
    month = request.GET.get('month')

    if employer_name or employer_number or year or month:
        pattern = ''
        dic = {}

        if employer_name:
            dic["name"] = 'e.employer_name like \'%' + employer_name.strip() + '%\''

        if employer_number:
            dic["number"] = 'e.employer_number like \'%' + employer_number.strip() + '%\''

        if year:
            dic["year"] = 'p.date like \'%' + year.strip() + '%\''

        if month:
            dic["month"] = 'MONTH(p.date) like \'%' + month.strip() + '%\''

        like_list = []
        for key in dic:
            like_list.append(dic[key])

        like_query = ' AND '.join(like_list)

        print("Query ", like_query)

        conn = mysql.connector.connect(user=database_username, password=database_password, host=database_ip,
                                       database=database_name)
        cursor = conn.cursor()
        cursor.execute(
            'select e.employer_number, e.employer_name, p.amount, p.date from '
            'employers e left join payments p on e.employer_number = p.employer_number where ' + like_query)
        data_list = cursor.fetchall()
        conn.close()
        return render(request, 'collections.html', {'collections': data_list})
    else:
        return render(request, 'collections.html')


def get_master_data(request):
    conn = mysql.connector.connect(user=database_username, password=database_password, host=database_ip,
                                   database=database_name)
    cursor = conn.cursor()
    cursor.execute(
        'select * from collections')
    data_list = cursor.fetchall()
    conn.close()
    print(data_list)
    return render(request, 'master_file.html', {'collections': data_list})


def detail(request, employer_id):
    return HttpResponse("You're looking at employer %s. " % employer_id)


def results(request, employer_id):
    response = "You're looking at the results of employer %s."
    return HttpResponse(response % employer_id)


def comment(request, employer_id):
    return HttpResponse("You're commenting on employer %s." % employer_id)
