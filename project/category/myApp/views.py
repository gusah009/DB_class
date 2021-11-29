from django.shortcuts import get_object_or_404, render, redirect

from myApp.forms import PostForm
from .models import Students

# Create your views here.
def main(request):
  students = Students.objects.all()
  return render(request, 'myApp/assignment1_main.html', {"students": students})

def create(request):

  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')

  else:
    form = PostForm()
  return render(request, 'myApp/assignment1_newRecord.html', {"form": form})

def search(request, keyword):
  students = Students.objects.all()
  return render(request, 'myApp/assignment1_search.html', {"students": students})

def edit(request, student_id):
  student = get_object_or_404(Students, student_id=student_id)

  if request.method == 'POST':
    form = PostForm(request.POST, instance=student)
    if form.is_valid():
      form.save()
      return redirect('home')

  else:
    form = PostForm(instance=student)
  return render(request, 'myApp/assignment1_updateRecord.html', {"form": form})

def delete(request, student_id):
  student = Students.objects.get(student_id=student_id)
  student.delete()
  return render(request, 'myApp/assignment1_deleteRecord.html', {"student": student})


