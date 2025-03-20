import praw
import requests
import os
import json
import re

# Função para remover caracteres inválidos e extrair somente a parte útil do URL
def sanitize_filename(filename):
    # Se existir uma query na URL, extraia apenas a parte antes do '?'
    if '?' in filename:
        filename = filename.split('?')[0]
    return filename

HISTORY_PATH="history/reddit"
os.makedirs(HISTORY_PATH, exist_ok=True)

CREDENTIALS_PATH="credentials/reddit_credentials.json"
with open(CREDENTIALS_PATH, "r") as credentials_file:
    credentials = json.load(credentials_file)

# Credenciais do Reddit
CLIENT_ID=credentials["client_id"]
CLIENT_SECRET=credentials["client_secret"]
USER_AGENT=credentials["user_agent"]

# Inicializa o PRAW
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Escolhe subreddit
subreddit = reddit.subreddit("HonkaiStarRail")

# Cria pasta para salvar mídia
MEDIA_PATH = "media/reddit"
os.makedirs(MEDIA_PATH, exist_ok=True)

# Caminho do arquivo que armazena os IDs de posts já visualizados
CHECKED_POSTS_PATH = "history/reddit/reddit_checked_posts.txt"
if not os.path.exists(CHECKED_POSTS_PATH):
    open(CHECKED_POSTS_PATH, "w").close()

checked_posts = set()

# Função para checar posts
def check_posts(limit=1):
    UNCHECKED_POSTS = []

    with open(CHECKED_POSTS_PATH, "r") as checked_posts_file:
        checked_posts=checked_posts_file.read().splitlines()

    for post in subreddit.hot(limit=limit):

        if post.id in checked_posts:
            print(f"Post já visualizado: {post.id}")
            continue # Ignora posts já vistos
        
        print("Título: ", post.title)
        print("URL: ", post.url)

        saved_media = 0  # Contador de mídia do post

        # Se o post for uma única imagem
        if post.url.endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4")):
            file_extension = os.path.splitext(post.url)[-1]
            media_url = post.url
            media_name = f"{MEDIA_PATH}/{post.id}_{file_extension}"
            media_name = sanitize_filename(media_name)

            # Baixa mídia
            response = requests.get(media_url)
            with open(media_name, "wb") as media_file:
                media_file.write(response.content)
            
            saved_media += 1
            print(f"✅ Mídia salva: {media_name}")
        
        # Se o post conter mais de uma mídia
        elif hasattr(post, "gallery_data") and post.gallery_data:
            for index, item in enumerate(post.gallery_data["items"]):
                media_id = item["media_id"]

                if media_id in post.media_metadata:
                    media_url = post.media_metadata[media_id]["s"]["u"]
                    media_url = media_url.replace("&amp", "&")  # Correção de caracteres HTML no link
                    file_extension = os.path.splitext(media_url)[-1]

                    # Arquivo de saída
                    media_name = f"{MEDIA_PATH}/{post.id}_{index+1}.{file_extension}"
                    media_name = sanitize_filename(media_name)

                    response = requests.get(media_url)
                    with open(media_name, "wb") as media_file:
                        media_file.write(response.content)
                    
                    print(f"✅ Mídia salva: {media_name}")
                
                else:
                    print(f"⚠️ Erro ao obter mídia para {media_id}")
        
        if saved_media == 0:
            print("⚠️ Não foi encontrada mídia para esse post")
        
        print("-" * 30)

        UNCHECKED_POSTS.append(
                {"id":post.id,
                 "author":post.author.name,
                 "title": post.title,
                 "content": post.selftext
                 })

        with open(CHECKED_POSTS_PATH, "a") as checked_posts_file:
            checked_posts_file.write(post.id + "\n")

    return UNCHECKED_POSTS