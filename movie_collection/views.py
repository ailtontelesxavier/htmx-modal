import json

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator

from .models import Movie
from .forms import MovieForm

class index(ListView):

    template_name = "index.html"
    model = Movie
    paginate_by = 5


#def index(request):
#    return render(request, 'index.html')


class movie_list(ListView):
    #template_name = 'movie_list.html'
    model = Movie
    paginate_by = 5
    
    def get_template_names(self):
        if self.request.htmx:
            print("aqui 1")
            return 'movie_list.html'
        
        print('aqui 2')
        return 'index.html'
    

    
def add_movie(request):
    
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{movie.title} added.",
                    })
                })
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {
        'form': form,
    })


def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": f"{movie.title} updated."
                    })
                }
            )
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie_form.html', {
        'form': form,
        'movie': movie,
    })


@ require_POST
def remove_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "movieListChanged": None,
                "showMessage": f"{movie.title} deleted."
            })
        })
