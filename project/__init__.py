# project/__init__.py


import os
from flask import Flask, jsonify, make_response, request, Response
from reportlab.pdfgen import canvas
import io
import urllib.request
import json
from reportlab.pdfbase.pdfmetrics import stringWidth
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask_mail import Mail, Message


# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'uwallet6@gmail.com',
	MAIL_PASSWORD = 'unal12345'
	)

mail=Mail(app)

@app.route('/json/<correo>', methods=['POST'])
def pdf2(correo):

    output = io.BytesIO()
    p = canvas.Canvas("/usr/src/app/project/extractos.pdf")

    data = request.get_json()

    envios_recibidos =  data[u'total_receive']
    envios_realizados = data[u'total_send']
    cargas_tarjeta = data[u'total_load']


    p.setFont('Helvetica-Bold', 10)
    p.drawString(20, 810, "Cargas desde tarjeta....... "+str(cargas_tarjeta))
    p.drawString(20, 795, "Envios recibidos........... "+str(envios_recibidos))
    p.drawString(20, 780, "Envios realizados.......... "+str(envios_realizados))

    #Nombres de columna de DINERO RECIBIDO
    p.setFont('Helvetica-Bold', 12)
    p.drawString(15, 755, "DINERO RECIBIDO:")
    p.setFont('Helvetica-Bold', 10)
    p.drawString(20, 740, "N. Transacción")
    p.drawString(110, 740, "Remitente")
    p.drawString(210, 740, "Monto")
    p.drawString(300, 740, "Estado")
    p.drawString(370, 740, "Fecha")
    p.drawString(470, 740, "Hora")

    aux = 695-15*(envios_recibidos)
    #Nombres de columna de DINERO ENVIADO
    p.setFont('Helvetica-Bold', 12)
    p.drawString(15, aux+15, "DINERO ENVIADO:")
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

    #p.showPage()
    p.save()

    msg = Message("Extractos", sender="uwallet6@gmail.com", recipients=[correo])

    with app.open_resource("extractos.pdf") as fp:
        msg.attach("extractos.pdf","application/pdf", fp.read())

    mail.send(msg)


    pdf_out = output.getvalue()
    output.close()
    return "Sent"

@app.route('/json2/<correo>/<int:i_dia>/<int:i_mes>/<int:i_anno>/<int:f_dia>/<int:f_mes>/<int:f_anno>', methods=['POST'])
def pdf3(correo,i_dia,i_mes,i_anno,f_dia,f_mes,f_anno):
  output = io.BytesIO()
  p = canvas.Canvas("/usr/src/app/project/extractos.pdf")

  data = request.get_json()
  fecha_inicial = str(i_anno)+"-"
  if(len(str(i_mes))==1):
    fecha_inicial += "0"
  fecha_inicial += str(i_mes)+"-"
  if(len(str(i_dia))==1):
    fecha_inicial += "0"
  fecha_inicial += str(i_dia)+"T00:00:00.000Z"

  fecha_final = str(f_anno)+"-"
  if(len(str(f_mes))==1):
    fecha_final += "0"
  fecha_final += str(f_mes)+"-"
  if(len(str(f_dia))==1):
    fecha_final += "0"
  fecha_final += str(f_dia)+"T99:99:99.999Z"

  envios_recibidos =  data[u'total_receive']
  envios_realizados = data[u'total_send']
  cargas_tarjeta = data[u'total_load']

  p.setFont('Helvetica-Bold', 10)

  #Nombres de columna de DINERO RECIBIDO
  p.setFont('Helvetica-Bold', 12)
  p.drawString(15, 755, "DINERO RECIBIDO:")
  p.setFont('Helvetica-Bold', 10)
  p.drawString(20, 740, "N. Transacción")
  p.drawString(110, 740, "Remitente")
  p.drawString(210, 740, "Monto")
  p.drawString(300, 740, "Estado")
  p.drawString(370, 740, "Fecha")
  p.drawString(470, 740, "Hora")

  aux = 695-15*(envios_recibidos)
  #Nombres de columna de DINERO ENVIADO
  p.setFont('Helvetica-Bold', 12)
  p.drawString(15, aux+15, "DINERO ENVIADO:")
  p.setFont('Helvetica-Bold', 10)
  p.drawString(20, aux, "N. Transacción")
  p.drawString(110, aux, "Destinatario")
  p.drawString(210, aux, "Monto")
  p.drawString(300, aux, "Estado")
  p.drawString(370, aux, "Fecha")
  p.drawString(470, aux, "Hora")
  total_recibidos_pdf = 0
  total_enviados_pdf = 0
  total_cargas_pdf = 0

  p.setFont('Helvetica', 9)
  fila = 15
  for i in range(0, len(data[u'list_receive'])):
    if(str(data[u'list_receive'][i][u'updated_at'])<fecha_final and str(data[u'list_receive'][i][u'updated_at'])>fecha_inicial):
      total_recibidos_pdf +=1
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
    if(str(data[u'list_send'][i][u'updated_at'])<fecha_final and str(data[u'list_send'][i][u'updated_at'])>fecha_inicial):
      total_enviados_pdf +=1
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
    if(str(data[u'list_load'][i][u'updated_at'])<fecha_final and str(data[u'list_load'][i][u'updated_at'])>fecha_inicial):
      total_cargas_pdf +=1
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


  p.drawString(20, 810, "Cargas desde tarjeta....... "+str(total_cargas_pdf))
  p.drawString(20, 795, "Envios recibidos........... "+str(total_recibidos_pdf))
  p.drawString(20, 780, "Envios realizados.......... "+str(total_enviados_pdf))

  p.save()
  msg = Message("Extractos "+fecha_inicial[0:10]+"---"+fecha_final[0:10], sender="uwallet6@gmail.com", recipients=[correo])



  msg.body = "Transacciones realizadas entre la fecha: "+fecha_inicial[0:10] +" y la fecha "+fecha_final[0:10]+".\n"+"Gracias por usar UWalllet."

  with app.open_resource("extractos.pdf") as fp:
    msg.attach("extractos.pdf","application/pdf", fp.read())

  mail.send(msg)
  pdf_out = output.getvalue()
  output.close()
  return "Sent"
