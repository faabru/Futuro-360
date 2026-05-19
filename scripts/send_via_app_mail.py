import sys, os
sys.path.insert(0, os.getcwd())
from app import enviar_email, app
from flask_mail import Message

with app.app_context():
    msg = Message(
        subject='Prueba desde app.enviar_email',
        recipients=['test@example.com'],
    )
    msg.body = 'Cuerpo de prueba en texto'
    msg.html = '<p>Cuerpo <strong>HTML</strong> de prueba</p>'

    try:
        enviar_email(msg)
        print('Se ejecutó enviar_email() correctamente')
    except Exception as e:
        print('Error al ejecutar enviar_email():', e)
