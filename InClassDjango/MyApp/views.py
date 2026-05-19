from .models import teacher
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from pypdf import PdfReader, PdfWriter
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from django.contrib.staticfiles.storage import staticfiles_storage
from .forms import InputForm

import io
import shutil
import re
import itertools

task_weights = []

# Create your views here.
def index(request):
    teach = teacher.objects.all()

    return render(request, "MyApp/index.html",{'content': teach})

def input_view(request):
    if request.method == "POST":

        form = InputForm(request.POST,request.FILES)
        if form.is_valid():
            
            file_content = request.FILES['PDF_File']
            file_content.read()
            pdf_stream = io.BytesIO(b"file_content")
            form.save()
            reader = PdfReader(file_content)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            text = page.extract_text()
            #print(text)
            task_weights = re.findall("(" + r'\d{2}' + "%" + ")", text)
            task_weights = list(set(task_weights))
            tasks = []
            upper = 0
            for i in range(len(task_weights)):
                tasks.append(re.findall(rf"\w+\s\({task_weights[i]}\)" '|' rf"[a-zA-Z]+\s[a-z]+\s\({task_weights[i]}\)", text))
            tasks = list(itertools.chain(*tasks))
            for i in range(len(tasks)):
                for j in tasks[i]:
                    if j.isupper():
                        upper += 1
                if upper <= 2:
                    tasks[i] = re.sub(r".*(?=[A-Z])", "", str(tasks[i]))
                upper = 0
            sorted_tasks = sorted(tasks, key = text.find)
            split_names = []
            for i in range(len(sorted_tasks)):
                split_names.append(sorted_tasks[i].split("("))
            split_tasks = list(itertools.chain(*split_names))
            for i in range(len(split_tasks)):
                if split_tasks[i].endswith(")"):
                    split_tasks[i] = re.sub(r"\)", "", str(split_tasks[i]))

            #teacher.objects.create(task1 = split_tasks[0], task1_weight = split_tasks[1], task2 = split_tasks[2], task2_weight = split_tasks[3], task3 = split_tasks[4], task3_weight = split_tasks[5], task4 = split_tasks[6], task4_weight = split_tasks[7])
            # ^ should work but gives null error for teacher.VET
            teacher.task1 = split_tasks[0]
            teacher.task1_weight = split_tasks[1]
            teacher.task2 = split_tasks[2]
            teacher.task2_weight = split_tasks[3]
            teacher.task3 = split_tasks[4]
            teacher.task3_weight = split_tasks[5]
            teacher.task4 = split_tasks[6]
            teacher.task4_weight = split_tasks[7]

            print("task 1 = " + teacher.task1)
            print("task 1 weight = " + teacher.task1_weight)
            print("task 2 = " +  teacher.task2)
            print("task 2 weight = " + teacher.task2_weight)
            print("task 3 = " + teacher.task3)
            print("task 3 weight = " + teacher.task3_weight)
            print("task 4 = " + teacher.task4)
            print("task 4 weight = " + teacher.task4_weight)

            #txtFile = HttpResponse(text, content_type = 'text/plain')  #download txt doc for esier time cheaking data from pdf 
            #txtFile['Content-Disposition'] = 'attachment; filename="data.txt"'
            #txtFile.write(text)
            #return txtFile
            
            return redirect('index')

    else:

        form = InputForm()

    return render(request, "MyApp/input.html", {"form": form})

def report(request, file_content):
    pdf_file = file_content

    try:
        merger = PdfWriter()

        input1 = PdfReader(gen_pdf())
        input2 = PdfReader(pdf_file, "rb")

        merger.append(input1)
        merger.append(input2)

        buffer = io.BytesIO()
        merger.write(buffer)
        buffer.seek(0)

        response = FileResponse(buffer, as_attachment=True, filename="Attachment.pdf")
    except FileNotFoundError:
        response = FileResponse(gen_pdf(), as_attachment=True, filename="noFile.pdf")

    return response

def gen_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    lines = [('Name:', 'Teaching Area:')]

    teachers = teacher.objects.all()

    for teach in teachers:
        lines.append(teach.Name, teach.Area)

    table = Table(lines)
    table.wrapOn(p, 300, 300)
    table.drawOn(p, 10, 650)

    p.showPage()
    p.save()

    buffer.seek(0)
    return(buffer)
