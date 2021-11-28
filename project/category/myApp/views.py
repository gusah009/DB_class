from django.shortcuts import render
from .models import Students

# Create your views here.
def main(request):
  students = Students.objects.all()
  return render(request, 'myApp/assignment1_main.html', {"students": students})

def create(request):
  students = Students.objects.all()
  return render(request, 'myApp/assignment1_newRecord.html', {"students": students})

def search(request, keyword):
  students = Students.objects.all()
  return render(request, 'myApp/assignment1_search.html', {"students": students})

def edit(request, student_id):
  students = Students.objects.all()
  return render(request, 'myApp/assignment1_updateRecord.html', {"students": students})


