from cowinner.settings import MEDIA_ROOT
from django.db.models import query
# from django.http.response import HttpResponse
from django.http.response import Http404, HttpResponse
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from . views_get import *
from . models import *
from django.conf import settings
from django.http import JsonResponse
from django.utils.encoding import force_text, smart_str
from django.views.static import serve
import os, tempfile, zipfile
import http.client
import json
import hashlib
import pprint
import json
import fitz
from cowinner.settings import BASE_DIR

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
            elif report_type == 'confirm_otp_form':
                print('confirm_otp called!')
                data = confirm_otp(request)
                return Response(data)
            elif report_type == "download_form":
                print('ULALALALA ULALA ULALA ULALA')
                data = download_certificate(request)
                return Response(data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
global txn
txn = ""

global bearer_token
bearer_token = ""
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
        global txn
        txn = txn_id
        return "ok" 
    except Exception as e:
        print(e)
        return "not_ok"
    
def sha_hash(otp):
    str = otp
    result = hashlib.sha256(str.encode())
    hexdecimal = result.hexdigest()
    return hexdecimal

def confirm_otp(request):
    try:
        # data = data.decode("utf-8")
        data = dict(request.data)
        
        global txn
        print ("txn:", txn,'\n')
        txnID = txn
        print ('\ndata from confirm OTP page:\n',data)
        print('==============================================================================')
        for k in data:
            print (k,'-', data[k][0])
        print('==============================================================================')
        otp = data["otp"][0]
        # hash with SHA 256
        otp = sha_hash(otp)
        
        beneficiary_id = data['beneficiary_id'][0]
        
        payload = json.dumps({
        "otp": str(otp),
        "txnId": txnID
        })
        headers = {
        'Content-Type': 'application/json'
        }
        print('payload:', payload)
        print('headers:', headers)
        print('==============================================================================')
        
        conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
        conn.request("POST", "/api/v2/auth/public/confirmOTP", payload, headers)
        res = conn.getresponse()
        print ('res:',res)
        print('==============================================================================')
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        print ('data:',data)
        print('type(data) after decode:', type(data))
        print('==============================================================================')
        token = data["token"]
        print ('token after conversion:', token)
        print('==============================================================================')
        global bearer_token
        bearer_token = token
        g_response = generate_certificate(bearer_token, beneficiary_id)
        if (len(str(g_response)) <= 100):
            return "b_id_not_exist"
        else:
            fileresponse = g_response
            file = open(os.path.join(MEDIA_ROOT,"certificates","certificate.pdf"), 'wb')
            file.write(fileresponse)
            file.close()
            file_name = os.path.join(MEDIA_ROOT,"certificates","certificate.pdf")
            path_to_file = file_name
            print('===========================================================================')
            print('path_to_file', path_to_file)
            print('===========================================================================')
            my_file_url = os.path.join(MEDIA_ROOT, "certificates", "certificate.pdf")
            context = {
                'my_file_url' : my_file_url
            }               
            return "ok"
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

def generate_certificate(bearer_token, beneficiary_id):
    token = bearer_token
    conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
    payload = ''
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    conn.request("GET", "/api/v2/registration/certificate/public/download?beneficiary_reference_id={}".format(beneficiary_id), payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data
# from io import BytesIO
def download_certificate(request):
    print('ENTERED THE download_certificate FUNCTION')
    filepath = os.path.join(MEDIA_ROOT, 'certificates', 'certificate.pdf')
    text = ''
    try:
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.getText()
                    
        if (len(text) < 1):
            return "too_short"
        else:
            if ("COVAXIN" in text):
                print("COVAXIN")
                return "COVAXIN"
            elif("COVISHIELD" in text):
                return "COVISHIELD"
            else:
                return "something_wrong"

    except Exception as e:
        print(e)
        print('Cannot open the fucking file!')
        return "cant_open_file"
    
