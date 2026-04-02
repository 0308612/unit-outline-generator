

from urllib import request, response
from xml.dom.minidom import Document
from .models import teacher
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from pypdf import PdfReader

from .models import teacher
from .forms import InputForm
import io

# Create your views here.
def index(request):
    teach = teacher.objects.all()

    return render(request, "MyApp/index.html",{'content': teach})

def input_view(request):

    if request.method == "POST":

        form = InputForm(request.POST)
        pdf_file = request.FILES['pdf_file']
        pdf_content = pdf_file.read()
        pdf_buffer = io.BytesIO(pdf_content)
        form.cleaned_data['PDF_File']
        reader = PdfReader(pdf_buffer)
        print(len(reader.pages))
        page = reader.pages[0]
        text = page.extract_text()
        print(text)

        if form.is_valid():

            form.save()
            return redirect('index')


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