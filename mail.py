import smtplib, os, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Credenciais do e-mail remetente
CREDENTIALS_PATH="credentials/email_credentials.json"
with open(CREDENTIALS_PATH, "r") as credentials_file:
    credentials=json.load(credentials_file)

def send_email(receiver="", subject="", content="", attachs=[]):
    sender=credentials["sender"]
    app_password=credentials["app_password"]
    
    # Se a função não recebe um receiver personalizado, utiliza por padrão o usado em credentials
    if not receiver:
        receiver = credentials["receiver"]

    # Cria o objeto MIMEMultipart para compor a mensagem
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    # Anexa o corpo do e-mail
    msg.attach(MIMEText(content, 'plain'))

    # Função para anexar arquivos à mensagem
    def attach_file(msg, file_path):
        if not os.path.exists(file_path):
            print(f"Arquivo não encontrado: {file_path}")
            return
        
        file_name = os.path.basename(file_path)

        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header("Content-Dispositionm", f"attachment; file_name={file_name}")
        msg.attach(part)
        print(f"Arquivo anexado: {file_name}")
    

    for file in attachs:
        attach_file(msg, file)
    
    email_text = msg.as_string()

    # Conectar ao servidor SMTP do Gmail e enviar o e-mail
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() # Inicia a conexão segura TLS
        server.login(sender, app_password)
        server.sendmail(sender, receiver, email_text)
        print("✅ E-mail enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
    finally:
        server.quit()