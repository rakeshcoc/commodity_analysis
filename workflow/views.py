from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
import requests,json,googlemaps
from .models import commodity_data,distance_table
from datetime import datetime
import math
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
# Create your views here.
key = "AIzaSyBnd0mAaz1-lihGN_psunPAcXmtJE6zzMw"
def index(request):
    if request.method == 'GET':
        return HttpResponse("Hello")
    else:
        return HttpResponse("Error")

def refresh_data(request):
    try:
        with open('workflow/file.txt') as json_file:
            data = json.load(json_file)
        print(len(data))
        for i in data:
            x = datetime.strptime(i['arrival_date'],"%d/%m/%Y")
            commodity_data.objects.create(arrival_date=x,state=i['state'],district =i['district'],market = i['market'],commodity=i['commodity'],variety=i['variety'],min_price=eval(i['min_price']),max_price=eval(i['max_price']),modal_price=eval(i['modal_price']))
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("Success")

def find_distance(source,destination):
    try:
        res = get_object_or_404(distance_table,source=source,destination=destination)
    except Exception:
        try:
            res = get_object_or_404(distance_table,source=destination,destination=source)
        except Exception:
            print("Not found")
            gmaps = googlemaps.Client(key=key)
            dist = gmaps.distance_matrix(source,destination)['rows'][0]['elements'][0]
            print(dist)
            net_distance = math.ceil(dist['distance']['value']/1000)
            distance_table.objects.create(source=source,destination=destination,distance=float(net_distance))
            return net_distance
        print("Found")
        return res.distance
    print("Found")
    return res.distance

def best_to_trade(data):
    price_difference = []
    for i in range(len(data)-1):
        temp ={}
        j = i+1
        source = data[i]['market']+" "+data[i]['district']+" "+data[i]['state']
        src_price = data[i]['modal_price']
        temp[source] = []
        while(j < len(data)):
            destination = data[j]['market']+" "+data[j]['district']+" "+data[j]['state']
            des_price = data[j]['modal_price']
            distance = find_distance(source,destination)
            if des_price-src_price >0:
                temp[source].append((destination,des_price-src_price,distance)) 
            j += 1
        price_difference.append(temp)
    return price_difference

class search_query(APIView):
    def post(self,request):
        state = request.data['state']
        commodity = request.data['commodity']
        variety = request.data['variety']
        res = commodity_data.objects.all().filter(state=state,commodity=commodity,variety=variety).order_by('modal_price').values()
        x = []
        for i in res:
            x.append(i)
        res = best_to_trade(x)
        return Response(res)