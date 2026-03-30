from ast import ImportFrom
from urllib import request, response
from xml.dom.minidom import Document
from .models import teacher
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pypdf

from .models import teacher
from .forms import InputForm

# Create your views here.
def index(request):
    teach = teacher.objects.all()

    return render(request, "MyApp/index.html",{'content': teach})

def input_view(request):

    if request.method == "POST":

        form = ImportFrom(request.POST, request.FILES)

        if form.is_valid():

            form.save()

    else:

        form = InputForm()



    return render(request, "MyApp/input.html", {"form": form})

#def prosses_pdf_data(request, doc_id):
#    document = teacher.objects.get(id = doc_id)
#    with open(document.pdf_file.path, 'rb') as pdf_file_handle:
#        pdf_reader = pypdf.PdfReader(pdf_file_handle)
#        text_content = ""
#        for page in pdf_reader.pages:
#            text_content += page.extract_text()

#        return render(request, 'index.html', {'content':text_content})