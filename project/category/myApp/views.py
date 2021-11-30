from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
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
      return redirect('/')

  else:
    form = PostForm()
  return render(request, 'myApp/assignment1_newRecord.html', {"form": form})

def search(request, keyword):
  students = Students.objects.all()
  return render(request, 'myApp/assignment1_search.html', {"students": students})

def edit(request, id):
  student = get_object_or_404(Students, id=id)

  if request.method == 'POST':
    form = PostForm(request.POST, instance=student)
    if form.is_valid():
      form.save()
      return redirect('/')

  else:
    form = PostForm(instance=student)
  return render(request, 'myApp/assignment1_updateRecord.html', {"form": form})

def delete(request, id):
  student = Students.objects.get(id=id)
  student.delete()
  return redirect(reverse('assignment1_main'))


