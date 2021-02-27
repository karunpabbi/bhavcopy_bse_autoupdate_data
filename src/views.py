from django.shortcuts import render
from .models import *
from django.conf import settings
from django.contrib import messages
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import csv
import io


CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

def get_ticker(filter_ticker = None):
    if filter_ticker:
        print("DATA COMING FROM DB")
        
        tickers = Ticker.objects.filter(sc_name__contains = filter_ticker)
    else:
        tickers = Ticker.objects.all()
    return tickers


def home(request):
    
    filter_ticker = request.GET.get('ticker')
    if cache.get(filter_ticker):
        print("DATA COMING FROM CACHE")
        ticker = cache.get(filter_ticker)
    else:
        if filter_ticker:
            ticker = get_ticker(filter_ticker)
            cache.set(filter_ticker, ticker)
        else:
            ticker = get_ticker()
        
    context = {'ticker': ticker}
    return render(request, 'home.html' , context)
@csrf_exempt
def upload(request):
    
    prompt={
        'order':'ORDER SHOULD BE CORRECT'
    }
    
    if request.method == "GET":
        return render(request, 'upload.html' , prompt)
    
    csv_file=request.FILES['file']
    
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THis is not correct file format')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    print("Removing Old Data")
    Ticker.objects.all().delete()
    print("Adding Updated Data")
    for column in csv.reader(io_string,delimiter=',',quotechar="|"):
        _, created = Ticker.objects.update_or_create(
            sc_code=column[0],
            sc_name=column[1],
            sc_open=column[4],
            sc_high=column[5],
            sc_low=column[6],
            sc_close=column[7],
        )
    
    # with open(csv_file) as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         p = Ticker(sc_code=row['SC_CODE'], sc_name=row['SC_NAME'], sc_open=row['OPEN'], sc_high=row['HIGH'], sc_low=row['LOW'], sc_close=row['CLOSE'])
    #         p.save()
            
        context = {}
    return render(request, 'upload.html' , context)
    