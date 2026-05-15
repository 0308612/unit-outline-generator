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

task_weights = []

# Create your views here.
def index(request):
    teach = teacher.objects.all()

    return render(request, "MyApp/index.html",{'content': teach})

def input_view(request):
    #dates = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"] #for due date finding
    #days = [" 01"," 02"," 03"," 04"," 05"," 06"," 07"," 08"," 09"," 10"," 11"," 12"," 13"," 14"," 15"," 16"," 17"," 18"," 19"," 20"," 21"," 22"," 23"," 24"," 25"," 26"," 27"," 28"," 29"," 30"," 31"]
    if request.method == "POST":

        form = InputForm(request.POST,request.FILES)

        if form.is_valid():
            
            file_content = request.FILES['PDF_File']
            file_content.read()
            pdf_stream = io.BytesIO(b"file_content")

            reader = PdfReader(file_content)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            text = page.extract_text()
            #print(text)
            form.save()
            task_weights = re.findall("(" + r'\d{2}' + "%" + ")", text)
            print(task_weights)
            tasks = []
            upper = 0
            for i in range(len(task_weights)):
                tasks.append(re.findall(rf"[a-zA-Z]+\s\({task_weights[i]}\)" '|' rf"[a-zA-Z]+\s[a-zA-Z]+\s\({task_weights[i]}\)", text))
            for i in range(len(tasks)):
                for j in range(len(tasks[i])):
                    if j.isupper():
                        upper += 1
                if upper >= 2 and tasks[i].count(" ") > 2:
                    tasks[i] = re.sub(r".*(?=[A-Z])", "", str(tasks[i]))
                upper = 0
            print(tasks)


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
