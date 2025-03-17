import reddit, twitter, os

POSTS_FILE="twitter_posted.txt"

def run():
    posts = reddit.check_posts(1) # Verifica se há novos posts no Reddit

    # Lê arquivo de posts já publicados
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "w") as posts_file:
            pass # Se não existir, cria arquivo vazio

    with open(POSTS_FILE, "r") as posts_file:
            twitter_post_list = posts_file.read().splitlines()

    # Se houver posts novos, deve executar o passo do Twitter/X e Email
    for post in posts:
        if post["id"] not in twitter_post_list:
            twitter.send_post(post)

            with open(POSTS_FILE, "a") as posts_file:
                posts_file.write(f"\n{post["id"]}")

run()