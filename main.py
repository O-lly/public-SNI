import reddit, twitter, mail, schedule, time, os

RUNNING=True
TIME=0
POSTS_FILE="twitter_posted.txt"

# Lê arquivo de posts já publicados
if not os.path.exists(POSTS_FILE):
    with open(POSTS_FILE, "w") as posts_file:
        pass # Se não existir, cria arquivo vazio

with open(POSTS_FILE, "r") as posts_file:
    twitter_post_list = posts_file.read().splitlines()

def run():
    posts = reddit.check_posts(3) # Verifica se há novos posts no Reddit

    # Se houver posts novos, deve executar o passo do Twitter/X e Email
    for post in posts:
        if post["id"] not in twitter_post_list:
            time.sleep(1)
            
            twitter.send_post(post)

            with open(POSTS_FILE, "a") as posts_file:
                posts_file.write(f"{post["id"]}\n")

            email_text="Olá,\n\nHá um novo post no Reddit."
            mail.send_email(subject=post["title"], content=email_text)


# Agenda a tarefa para executar a cada 1 minuto
schedule.every(1).minutes.do(run)

while RUNNING:
    schedule.run_pending() # Executa a rotina se o horário for atingido
    time.sleep(1)
    TIME += 1
    if TIME % 10 == 0: 
        print(f"tempo decorrido: {TIME} segundos")
    if TIME > 200:
        RUNNING=False