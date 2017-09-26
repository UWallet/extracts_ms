# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from generator.models import File
from generator.serializers import FileSerializer
from rest_framework.response import Response
from reportlab.pdfgen import canvas
import requests
import urllib
import json

# Create your views here.

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def archivos_list(request):
    if request.method == 'GET':
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

def id_list(request, pk):
    try:
        archivo = File.objects.get(pk=pk)
    except File.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = FileSerializer(archivo)
        return JSONResponse(serializer.data)




def extracts_all(request, pk):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="extractos.pdf"'
        p = canvas.Canvas(response)
        url = "http://192.168.99.101:3000/by_user_id?userid="+str(pk)
        response2 = urllib.urlopen(url)
        data = json.loads(response2.read())
        envios_recibidos =  data[u'total_receive']
        envios_realizados = data[u'total_send']
        p.drawString(10, 785, "Cantidad de envios recibidos....... "+str(envios_recibidos))
        p.drawString(10, 770, "Cantidad de envios realizados....... "+str(envios_realizados))
        p.drawString(10, 755, "ID")
        p.drawString(90, 755, "REMITENTE")
        p.drawString(200, 755, "MONTO")
        p.drawString(320, 755, "ESTADO")
        p.drawString(400, 755, "FECHA")
        p.drawString(500, 755, "HORA")

        aux = 740-15*(envios_recibidos)
        p.drawString(10, aux, "ID")
        p.drawString(90, aux, "DESTINATARIO")
        p.drawString(200, aux, "MONTO")
        p.drawString(320, aux, "ESTADO")
        p.drawString(400, aux, "FECHA")
        p.drawString(500, aux, "HORA")

        fila = 0
        for i in range(0, len(data[u'list_receive'])):
            p.drawString(10, 740-fila, str(data[u'list_receive'][i][u'id']))
            p.drawString(90, 740-fila, str(data[u'list_receive'][i][u'useridgiving']))
            p.drawString(200, 740-fila, str(data[u'list_receive'][i][u'amount']))
            p.drawString(320, 740-fila, str(data[u'list_receive'][i][u'state']))
            s_aux = str(data[u'list_receive'][i][u'updated_at'])
            hora = ""
            fecha = ""
            b_aux = 1
            for c in s_aux:
                if(c=='T'):
                    b_aux = 0
                elif(c=='Z'):
                    b_aux = 0
                elif(b_aux==1):
                    fecha += c
                else:
                    hora += c
            p.drawString(400, 740-fila, fecha)
            p.drawString(500, 740-fila, hora)
            fila += 15
        fila = 15
        for i in range(0, len(data[u'list_send'])):
            p.drawString(10, aux-fila, str(data[u'list_receive'][i][u'id']))
            p.drawString(90, aux-fila, str(data[u'list_receive'][i][u'useridreceiving']))
            p.drawString(200, aux-fila, str(data[u'list_receive'][i][u'amount']))
            p.drawString(320, aux-fila, str(data[u'list_receive'][i][u'state']))
            s_aux = str(data[u'list_receive'][i][u'updated_at'])
            hora = ""
            fecha = ""
            b_aux = 1
            for c in s_aux:
                if(c=='T'):
                    b_aux = 0
                elif(c=='Z'):
                    b_aux = 0
                elif(b_aux==1):
                    fecha += c
                else:
                    hora += c
            p.drawString(400, aux-fila, fecha)
            p.drawString(500, aux-fila, hora)
            fila += 15
        p.showPage()
        p.save()
        return response


def extracts_days(request, pk, pk2):
    if request.method == 'GET':
        print(pk)
        print(pk2)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="extractos.pdf"'
        p = canvas.Canvas(response)
        url = "http://192.168.99.101:3000/by_date?userid="+str(pk)+"&days="+str(pk2)
        response2 = urllib.urlopen(url)
        data = json.loads(response2.read())
        envios_recibidos =  data[u'total_receive']
        envios_realizados = data[u'total_send']
        p.drawString(10, 785, "Cantidad de envios recibidos....... "+str(envios_recibidos))
        p.drawString(10, 770, "Cantidad de envios realizados....... "+str(envios_realizados))
        p.drawString(10, 755, "ID")
        p.drawString(90, 755, "REMITENTE")
        p.drawString(200, 755, "MONTO")
        p.drawString(320, 755, "ESTADO")
        p.drawString(400, 755, "FECHA")
        p.drawString(500, 755, "HORA")

        aux = 740-15*(envios_recibidos)
        p.drawString(10, aux, "ID")
        p.drawString(90, aux, "DESTINATARIO")
        p.drawString(200, aux, "MONTO")
        p.drawString(320, aux, "ESTADO")
        p.drawString(400, aux, "FECHA")
        p.drawString(500, aux, "HORA")

        fila = 0
        for i in range(0, len(data[u'list_receive'])):
            p.drawString(10, 740-fila, str(data[u'list_receive'][i][u'id']))
            p.drawString(90, 740-fila, str(data[u'list_receive'][i][u'useridgiving']))
            p.drawString(200, 740-fila, str(data[u'list_receive'][i][u'amount']))
            p.drawString(320, 740-fila, str(data[u'list_receive'][i][u'state']))
            s_aux = str(data[u'list_receive'][i][u'updated_at'])
            hora = ""
            fecha = ""
            b_aux = 1
            for c in s_aux:
                if(c=='T'):
                    b_aux = 0
                elif(c=='Z'):
                    b_aux = 0
                elif(b_aux==1):
                    fecha += c
                else:
                    hora += c
            p.drawString(400, 740-fila, fecha)
            p.drawString(500, 740-fila, hora)
            fila += 15
        fila = 15
        for i in range(0, len(data[u'list_send'])):
            p.drawString(10, aux-fila, str(data[u'list_receive'][i][u'id']))
            p.drawString(90, aux-fila, str(data[u'list_receive'][i][u'useridreceiving']))
            p.drawString(200, aux-fila, str(data[u'list_receive'][i][u'amount']))
            p.drawString(320, aux-fila, str(data[u'list_receive'][i][u'state']))
            s_aux = str(data[u'list_receive'][i][u'updated_at'])
            hora = ""
            fecha = ""
            b_aux = 1
            for c in s_aux:
                if(c=='T'):
                    b_aux = 0
                elif(c=='Z'):
                    b_aux = 0
                elif(b_aux==1):
                    fecha += c
                else:
                    hora += c
            p.drawString(400, aux-fila, fecha)
            p.drawString(500, aux-fila, hora)
            fila += 15
        p.showPage()
        p.save()
        return response
