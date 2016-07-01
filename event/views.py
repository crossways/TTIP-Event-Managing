from django.shortcuts import render

# Create your views here.
def event_startingpage(request):
    return render(request, 'event/starting_page.html')