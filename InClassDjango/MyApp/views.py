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


# Create your views here.
def index(request):
    teach = teacher.objects.all()

    return render(request, "MyApp/index.html",{'content': teach})

def input_view(request):

    if request.method == "POST":

        form = InputForm(request.POST,request.FILES)
        #uploaded_file = InputForm(request.FILES['PDF_File'])

        #pdf_file = request.FILES.get('pdf_file')
        ##pdf_file = InputForm.cleaned_data['pdf_file'] #cleaned data doesn't exist
        #fs = FileSystemStorage
        #filename = fs.save(pdf_file.name, pdf_file)
        #with open(filename, "rb") as fh:
        #    memoryFile = io.BytesIO(fh.read())
        #if memoryFile:
        #    pdf_content = memoryFile.read()
        #    pdf_buffer = io.BytesIO(pdf_content)
        #    form.cleaned_data['PDF_File']
        #    reader = PdfReader(pdf_buffer)
        #    print(len(reader.pages))
        #    page = reader.pages[0]
        #    text = page.extract_text()
        #    print(text)

        if form.is_valid():

            file_content = form.cleaned_data['PDF_File'].read()
            pdf_stream = io.BytesIO(file_content)

            reader = PdfReader(pdf_stream)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            text = page.extract_text()
            print(text)
            form.save()
            response = HttpResponse(text, content_type = 'text/plain')
            response['pdf text'] = 'attachment; filename="data.txt"'
            return response, redirect('index')


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