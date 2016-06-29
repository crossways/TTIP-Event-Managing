from django.shortcuts import render

# Create your views here.

def landingpage_view(request):
    return render(request, 'landingpage/landingpage.html')