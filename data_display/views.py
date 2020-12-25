from django.shortcuts import render

# Create your views here.



# /home_map
def home_map(request):
    # print('+++++++++++', request.environ)
    return render(request, 'map_demo.html')

# /details
def date_move(request):
    # print('+++++++++++', request.environ)
    return render(request, 'date_move.html')

