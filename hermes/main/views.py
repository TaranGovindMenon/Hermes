from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def student_index(request):
    return render(request, 'student_index.html')

def company_index(request): 
    return render(request, 'company_index.html')