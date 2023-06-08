from django.shortcuts import render, redirect
from .forms import AddFromCSVForm
# Create your views here.


def add_tasks_from_csv(request):
    if request.method == "POST":
        form = AddFromCSVForm(request.POST, request.FILES)
        if form.is_valid():

            # needs implementation
            return redirect('admin:index')
    else:
        form = AddFromCSVForm()
    # TODO: add file parsing, database modification and tests
    return render(request, 'admin/add_tasks_csv.html', {'form': form})