from logging import raiseExceptions
from xml.dom.minidom import Document
from .models import teacher
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pypdf import PdfReader
from pathlib import Path

from .models import teacher
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
            #matches = []
            #for month in dates:
            #    for day in days:
            #        matches.append(re.findall(day, text))
            #    matches.append(re.findall(month, text))
            task_weights = re.findall("(" + r'\d{2}' + "%" + ")", text)
            print(task_weights)
            #txtFile = HttpResponse(text, content_type = 'text/plain')  #download txt doc for esier time taking data from pdf 
            #txtFile['Content-Disposition'] = 'attachment; filename="data.txt"'
            #txtFile.write(text)
            #return txtFile
            return redirect('index')


    else:

        form = InputForm()



    return render(request, "MyApp/input.html", {"form": form})
