from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from . views_get import *
from . models import *
from django.conf import settings
from django.http import JsonResponse

import http.client
import json
import hashlib
import pprint
import json

@api_view(['POST'])
def post(request):
    if request.method == 'POST':
        report_type = request.query_params.get('report_type', None)
        print('\nreport_type: ',report_type, '\n')
        try:
            if report_type == 'send_otp':
                # print('send_otp is called!')
                data = send_otp(request)
                return Response(data)
            elif report_type == 'confirm_otp':
                data = confirm_otp(request)
                return Response(data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        

def send_otp(request):
    try:
        data = dict(request.data)
        # data = {k:v[0] for k, v in data.items() if k!='csrfmiddlewaretoken'}
        print('\ndata:\n',data,'\n')
        mobile = data['phone'][0]
        mobile = str(mobile)
        print('Your Phone Number:',mobile)
        conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
        payload = json.dumps({
            "mobile": mobile
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/v2/auth/public/generateOTP", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")  
        print(data)
        txn_id = json.loads(data)
        txn_id = txn_id["txnId"]
        print ('Transaction ID:',txn_id)
        return "ok" 
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
def sha_hash(otp):
    str = otp
    result = hashlib.sha256(str.encode())
    hexdecimal = result.hexdigest()
    return hexdecimal

def confirm_otp(request):
    try:
        data = dict(request.data)
        print('\ndata:\n',data,'\n')
        return "ok"
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)