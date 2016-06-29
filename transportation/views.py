from django.shortcuts import render

# Create your views here.

def transportation_startingpage(request):
    return render(request, 'transportation/starting_page.html')