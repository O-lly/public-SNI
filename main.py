import reddit

def run():
    posts = reddit.check_posts() # Verifica se há novos posts no Reddit

    # Se houver posts novos, deve executar o passo do Twitter/X e Email
    if posts:
        #send_tweet()
        #send_email()
        print(posts)

run()