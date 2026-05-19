import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

print('Usando MAIL_USERNAME:', MAIL_USERNAME)
print('Usando MAIL_PASSWORD length:', len(MAIL_PASSWORD) if MAIL_PASSWORD else 'None')

msg = EmailMessage()
msg['Subject'] = 'Prueba SMTP desde script'
msg['From'] = MAIL_USERNAME
msg['To'] = MAIL_USERNAME
msg.set_content('Este es un email de prueba enviado desde send_test_email.py')

try:
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=20) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(MAIL_USERNAME, MAIL_PASSWORD)
        s.send_message(msg)
    print('Email enviado correctamente')
except Exception as e:
    print('Error al enviar email:', repr(e))
    # Si es SMTPAuthenticationError, mostrar atributos si existen
    try:
        import smtplib as _s
        if isinstance(e, _s.SMTPAuthenticationError):
            print('SMTP error code:', e.smtp_code)
            print('SMTP error message:', e.smtp_error)
    except Exception:
        pass
