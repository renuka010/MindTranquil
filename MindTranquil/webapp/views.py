from django.shortcuts import render

# homepage
def index(request):
    return render(request, 'webapp/index.html')

#redirect to breathe
def breathe(request):
    return render(request, 'webapp/breathe.html')

#redirect to meditate
def meditate(request):
    return render(request, 'webapp/meditate.html')

#redirect to stats
def stats(request):
    return render(request, 'webapp/stats.html')
