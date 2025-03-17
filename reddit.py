import praw
import requests
import os

# Credenciais do Reddit
CLIENT_ID=""
CLIENT_SECRET=""
USER_AGENT=""

# Inicializa o PRAW
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Escolhe subreddit
subreddit = reddit.subreddit("HonkaiStarRail_leaks")

# Cria pasta para salvar mídia
MEDIA_PATH = "reddit_media"
os.makedirs(MEDIA_PATH, exist_ok=True)

# Caminho do arquivo que armazena os IDs de posts já visualizados
CHECKED_PATH = "checked_posts.txt"
UNCHECKED_POSTS = []

checked_posts = set()

# Carrega IDs de posts já verificados
if os.path.exists(CHECKED_PATH):
    with open(CHECKED_PATH, "r") as file:
        # Converte em conjunto para busca rápida
        checked_posts = set(file.read().splitlines)


# Função para checar posts
def check_posts(limit: int):
    for post in subreddit.new(limit=limit):

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
            media_name = f"{MEDIA_PATH}_{file_extension}"

            # Baixa mídia
            response = requests.get(media_url)
            with open(media_name, "wb") as media_file:
                media_file.write(response.content)
            
            saved_media += 1
            print(f"Mídia salva: {media_name}")
        
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

                    response = requests.get(media_url)
                    with open(media_name, "wb") as media_file:
                        media_file.write(response.content)
                    
                    print(f"Mídia salva: {media_name}")
                
                else:
                    print(f"Erro ao obter mídia para {media_id}")
        
        if saved_media == 0:
            print("Não foi encontrada mídia para esse post")
        
        print("-" * 30)

        UNCHECKED_POSTS.append(post.id)

        with open(checked_posts, "w") as checked_posts_file:
            checked_posts_file.write(post.id + "\n")

    return UNCHECKED_POSTS