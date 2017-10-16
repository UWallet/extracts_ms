# project/__init__.py


import os
from flask import Flask, jsonify, make_response, request
from reportlab.pdfgen import canvas
import io
import urllib.request
import json
from reportlab.pdfbase.pdfmetrics import stringWidth


# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


@app.route('/generateAll/<int:post_id>')
def pdf2(post_id):
    output = io.BytesIO()
    p = canvas.Canvas(output)

    url = "http://192.168.99.101:3000/by_user_id?userid="+str(post_id)
    response2 = urllib.request.urlopen(url)
    data = json.loads(response2.read())

    #variables envios
    envios_recibidos =  data[u'total_receive']
    envios_realizados = data[u'total_send']
    cargas_tarjeta = data[u'total_load']

    p.setFont('Helvetica-Bold', 10)
    #impresión cantidad de transacciones por tipo
    p.drawString(20, 810, "Cargas desde tarjeta....... "+str(cargas_tarjeta))
    p.drawString(20, 795, "Envios recibidos........... "+str(envios_recibidos))
    p.drawString(20, 780, "Envios realizados.......... "+str(envios_realizados))

    #Nombres de columna de envios
    p.setFont('Helvetica-Bold', 12)
    p.drawString(15, 755, "DINERO ENVIADO:")
    p.setFont('Helvetica-Bold', 10)
    p.drawString(20, 740, "N. Transacción")
    p.drawString(110, 740, "Remitente")
    p.drawString(210, 740, "Monto")
    p.drawString(300, 740, "Estado")
    p.drawString(370, 740, "Fecha")
    p.drawString(470, 740, "Hora")

    aux = 695-15*(envios_recibidos)
    #Nombres de columna de recibidos
    p.setFont('Helvetica-Bold', 12)
    p.drawString(15, aux+15, "DINERO RECIBIDO:")
    p.setFont('Helvetica-Bold', 10)
    p.drawString(20, aux, "N. Transacción")
    p.drawString(110, aux, "Destinatario")
    p.drawString(210, aux, "Monto")
    p.drawString(300, aux, "Estado")
    p.drawString(370, aux, "Fecha")
    p.drawString(470, aux, "Hora")

    p.setFont('Helvetica', 9)
    fila = 15
    for i in range(0, len(data[u'list_receive'])):
        tam_id = len(str(data[u'list_receive'][i][u'id']))
        p.drawString(24, 740-fila, ('0'*(10-tam_id))+str(data[u'list_receive'][i][u'id']))
        tam_id2 = len(str(data[u'list_receive'][i][u'useridgiving']))
        p.drawString(114, 740-fila, ('0'*(10-tam_id2))+str(data[u'list_receive'][i][u'useridgiving']))
        p.drawString(214, 740-fila, '$'+str(data[u'list_receive'][i][u'amount']))
        p.drawString(304, 740-fila, str(data[u'list_receive'][i][u'state']))
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
        p.drawString(374, 740-fila, fecha)
        p.drawString(474, 740-fila, hora)
        fila += 15

    fila = 15
    for i in range(0, len(data[u'list_send'])):
        tam_id = len(str(data[u'list_send'][i][u'id']))
        p.drawString(24, aux-fila, ('0'*(10-tam_id))+str(data[u'list_send'][i][u'id']))
        tam_id2 = len(str(data[u'list_send'][i][u'useridreceiving']))
        p.drawString(114, aux-fila, ('0'*(10-tam_id2))+str(data[u'list_send'][i][u'useridreceiving']))
        p.drawString(214, aux-fila, '$'+str(data[u'list_send'][i][u'amount']))
        p.drawString(304, aux-fila, str(data[u'list_send'][i][u'state']))
        s_aux = str(data[u'list_send'][i][u'updated_at'])
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
        p.drawString(374, aux-fila, fecha)
        p.drawString(474, aux-fila, hora)
        fila += 15

    aux = aux-fila-30
    p.setFont('Helvetica-Bold', 12)
    p.drawString(15, aux+15, "DINERO CARGADO DESDE LA TARJETA:")
    p.setFont('Helvetica-Bold', 10)
    #Nombres de columna de cargas desde tarjeta
    p.drawString(20, aux, "N. Transacción")
    p.drawString(210, aux, "Monto")
    p.drawString(300, aux, "Estado")
    p.drawString(370, aux, "Fecha")
    p.drawString(470, aux, "Hora")

    p.setFont('Helvetica', 9)
    fila = 15
    for i in range(0, len(data[u'list_load'])):
        tam_id = len(str(data[u'list_load'][i][u'id']))
        p.drawString(24, aux-fila, ('0'*(10-tam_id))+str(data[u'list_load'][i][u'id']))
        p.drawString(214, aux-fila, '$'+str(data[u'list_load'][i][u'amount']))
        p.drawString(304, aux-fila, str(data[u'list_load'][i][u'state']))
        s_aux = str(data[u'list_load'][i][u'updated_at'])
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
        p.drawString(374, aux-fila, fecha)
        p.drawString(474, aux-fila, hora)
        fila += 15


    p.showPage()
    p.save()

    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = "inline; filename=extractos.pdf"
    #response.mimetype = 'application/pdf'
    return response

@app.route('/generateDays/<int:user_id>/<int:days>')
def pdf3(user_id,days):
    output = io.BytesIO()
    p = canvas.Canvas(output)
    url = "http://192.168.99.101:3000/by_date?userid="+str(user_id)+"&days="+str(days)
    response2 = urllib.request.urlopen(url)
    data = json.loads(response2.read())

    #variables envios
    envios_recibidos =  data[u'total_receive']
    envios_realizados = data[u'total_send']
    cargas_tarjeta = data[u'total_load']

    p.setFont('Helvetica-Bold', 10)
    #impresión cantidad de transacciones por tipo
    p.drawString(20, 810, "Cargas desde tarjeta....... "+str(cargas_tarjeta))
    p.drawString(20, 795, "Envios recibidos........... "+str(envios_recibidos))
    p.drawString(20, 780, "Envios realizados.......... "+str(envios_realizados))

    #Nombres de columna de envios
    p.setFont('Helvetica-Bold', 12)
    p.drawString(15, 755, "DINERO ENVIADO:")
    p.setFont('Helvetica-Bold', 10)
    p.drawString(20, 740, "N. Transacción")
    p.drawString(110, 740, "Remitente")
    p.drawString(210, 740, "Monto")
    p.drawString(300, 740, "Estado")
    p.drawString(370, 740, "Fecha")
    p.drawString(470, 740, "Hora")

    aux = 695-15*(envios_recibidos)
    #Nombres de columna de recibidos
    p.setFont('Helvetica-Bold', 12)
    p.drawString(15, aux+15, "DINERO RECIBIDO:")
    p.setFont('Helvetica-Bold', 10)
    p.drawString(20, aux, "N. Transacción")
    p.drawString(110, aux, "Destinatario")
    p.drawString(210, aux, "Monto")
    p.drawString(300, aux, "Estado")
    p.drawString(370, aux, "Fecha")
    p.drawString(470, aux, "Hora")

    p.setFont('Helvetica', 9)
    fila = 15
    for i in range(0, len(data[u'list_receive'])):
        tam_id = len(str(data[u'list_receive'][i][u'id']))
        p.drawString(24, 740-fila, ('0'*(10-tam_id))+str(data[u'list_receive'][i][u'id']))
        tam_id2 = len(str(data[u'list_receive'][i][u'useridgiving']))
        p.drawString(114, 740-fila, ('0'*(10-tam_id2))+str(data[u'list_receive'][i][u'useridgiving']))
        p.drawString(214, 740-fila, '$'+str(data[u'list_receive'][i][u'amount']))
        p.drawString(304, 740-fila, str(data[u'list_receive'][i][u'state']))
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
        p.drawString(374, 740-fila, fecha)
        p.drawString(474, 740-fila, hora)
        fila += 15

    fila = 15
    for i in range(0, len(data[u'list_send'])):
        tam_id = len(str(data[u'list_send'][i][u'id']))
        p.drawString(24, aux-fila, ('0'*(10-tam_id))+str(data[u'list_send'][i][u'id']))
        tam_id2 = len(str(data[u'list_send'][i][u'useridreceiving']))
        p.drawString(114, aux-fila, ('0'*(10-tam_id2))+str(data[u'list_send'][i][u'useridreceiving']))
        p.drawString(214, aux-fila, '$'+str(data[u'list_send'][i][u'amount']))
        p.drawString(304, aux-fila, str(data[u'list_send'][i][u'state']))
        s_aux = str(data[u'list_send'][i][u'updated_at'])
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
        p.drawString(374, aux-fila, fecha)
        p.drawString(474, aux-fila, hora)
        fila += 15

    aux = aux-fila-30
    p.setFont('Helvetica-Bold', 12)
    p.drawString(15, aux+15, "DINERO CARGADO DESDE LA TARJETA:")
    p.setFont('Helvetica-Bold', 10)
    #Nombres de columna de cargas desde tarjeta
    p.drawString(20, aux, "N. Transacción")
    p.drawString(210, aux, "Monto")
    p.drawString(300, aux, "Estado")
    p.drawString(370, aux, "Fecha")
    p.drawString(470, aux, "Hora")

    p.setFont('Helvetica', 9)
    fila = 15
    for i in range(0, len(data[u'list_load'])):
        tam_id = len(str(data[u'list_load'][i][u'id']))
        p.drawString(24, aux-fila, ('0'*(10-tam_id))+str(data[u'list_load'][i][u'id']))
        p.drawString(214, aux-fila, '$'+str(data[u'list_load'][i][u'amount']))
        p.drawString(304, aux-fila, str(data[u'list_load'][i][u'state']))
        s_aux = str(data[u'list_load'][i][u'updated_at'])
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
        p.drawString(374, aux-fila, fecha)
        p.drawString(474, aux-fila, hora)
        fila += 15


    p.showPage()
    p.save()

    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = "inline; filename=extractos.pdf"
    #response.mimetype = 'application/pdf'
    return response
