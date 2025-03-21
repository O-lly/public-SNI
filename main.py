import reddit, twitter, mail, schedule, time, os, telegram_acc, asyncio, json

RUNNING=True

TWITTER_POSTS_FILE=twitter.CHECKED_POSTS_PATH
REDDIT_POSTS_FILE=reddit.CHECKED_POSTS_PATH
TELEGRAM_POSTS_FILE=telegram_acc.CHECKED_POSTS_PATH

CONFIG_FILE="config/config.json"
with open(CONFIG_FILE, "r") as config_file:
    config=json.load(config_file)

REDDIT_RECEIVE=config["reddit_receive"]
TWITTER_RECEIVE=config["twitter_receive"]
TELEGRAM_RECEIVE=config["telegram_receive"]

TWITTER_SEND=config["twitter_send"]
TELEGRAM_SEND=config["telegram_send"]
EMAIL_SEND=config["email_send"]

async def twitter_send_macro(post, self_posts):
    if post["id"] not in self_posts:
        time.sleep(1)
        twitter.send_post(post)
        with open(TWITTER_POSTS_FILE, "a") as twitter_posts_file:
            twitter_posts_file.write(f"{post['id']}\n")

async def mail_send_macro(subject, text):
    mail.send_email(subject=subject, content=text)

async def monitor():
    twitter_post_list = []
    telegram_post_list = []
    # Verifica posts já enviados para redes sob condição de executar o monitoramento de envio para essas redes
    if TWITTER_SEND:
        with open(TWITTER_POSTS_FILE, "r") as twitter_posts_file:
            twitter_post_list=twitter_posts_file.read().splitlines()

    if TELEGRAM_SEND:
        with open(TELEGRAM_POSTS_FILE, "r") as telegram_posts_file:
            telegram_post_list=telegram_posts_file.read().splitlines()

    # Monitora o recebimento de novos posts sob condição de poder receber posts
    if REDDIT_RECEIVE:
        reddit_posts=reddit.check_posts(config["reddit_limit"])
        
        # Se houver posts novos no Reddit, deve executar o passo de envio
        for post in reddit_posts:
            if TWITTER_SEND:
                await twitter_send_macro(post, twitter_post_list)
            if EMAIL_SEND:
                email_text=f"Olá,\n\nHá um novo post no Reddit."
                await mail_send_macro(subject=post["title"], text=email_text)
            
            """if TELEGRAM_SEND:
                if post["id"] not in telegram_post_list:
                    time.sleep()"""
    return
    

async def run():
    await monitor()

async def schedule_tasks():
    tempo = 0
    while RUNNING:
        tempo += 1
        schedule.run_pending()
        await asyncio.sleep(1)
        if tempo % 10 == 0:
            print(f"Tempo: {tempo} segundos.")
        if tempo == 200:
            break

async def main():
    # Agenda a execução da função run
    schedule.every(1).minutes.do(lambda: asyncio.create_task(run()))
    await schedule_tasks()  

if __name__ == "__main__":
    asyncio.run(main())  # ✅ Chama `asyncio.run()` apenas aqui