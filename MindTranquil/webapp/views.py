from django.shortcuts import render

# homepage
def index(request):
    return render(request, 'webapp/index.html')

#redirect to breathe
def breathe(request):
    return render(request, 'webapp/breathe.html')
