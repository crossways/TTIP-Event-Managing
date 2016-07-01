from django.shortcuts import render

# Create your views here.
def bednbreakfast_startingpage(request):
    return render(request, 'bednbreakfast/starting_page.html')