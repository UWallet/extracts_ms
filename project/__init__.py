# project/__init__.py


import os
from flask import Flask, jsonify, make_response, request
from reportlab.pdfgen import canvas
import io
import urllib.request
import json


# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


@app.route('/json', methods=['POST'])
def pdf2():
    output = io.BytesIO()
    p = canvas.Canvas(output)
    data     = request.get_json()
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
        p.drawString(10, aux-fila, str(data[u'list_send'][i][u'id']))
        p.drawString(90, aux-fila, str(data[u'list_send'][i][u'useridreceiving']))
        p.drawString(200, aux-fila, str(data[u'list_send'][i][u'amount']))
        p.drawString(320, aux-fila, str(data[u'list_send'][i][u'state']))
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
        p.drawString(400, aux-fila, fecha)
        p.drawString(500, aux-fila, hora)
        fila += 15

    p.showPage()
    p.save()

    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename=extractos.pdf"
    response.mimetype = 'application/pdf'
    return response
