

def run():
    posts = check_reddit() # Verifica se há novos posts no Reddit
    # Se houver posts novos, deve executar o passo do Twitter/X e Email
    if posts:
        send_tweet()
        send_email()