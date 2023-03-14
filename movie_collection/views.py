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


#def movie_list(request):
#    movie_list = Movie.objects.all()
#    paginator = Paginator(movie_list, 5)  # Show 25 contacts per page.
#
#    page_number = request.GET.get("page_number")
#    page_obj = paginator.get_page(page_number)
#    
#    return render(request, 'movie_list.html', {
#        'object_list': page_obj.object_list,
#        'page_obj': page_obj, 
#    })
   

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
    


#class add_movie(TemplateView):
#    template_name = 'movie_form.html'
#    model = Movie
#    def get(self, *args, **kwargs):
#        formset = BirdFormSet(queryset=Bird.objects.none())
#        return self.render_to_response({'bird_formset': formset})
#
#    # Define method to handle POST request
#    def post(self, *args, **kwargs):
#
#        formset = BirdFormSet(data=self.request.POST)
#
#        # Check if submitted forms are valid
#        if formset.is_valid():
#            formset.save()
#            return redirect(reverse_lazy("bird_list"))
#
#        return self.render_to_response({'bird_formset': formset})
    
    
    
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
