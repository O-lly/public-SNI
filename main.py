import reddit, twitter, mail, time, os, telegram_acc, asyncio, json

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
        await twitter.send_post(
            content=post["content"],
            media_gallery=post["media_gallery"]
        )
        with open(TWITTER_POSTS_FILE, "a") as twitter_posts_file:
            twitter_posts_file.write(f"{post['id']}\n")

async def mail_send_macro(subject, text):
    mail.send_email(subject=subject, content=text)

async def telegram_send_macro(post, self_posts):
    if post["id"] not in self_posts:
        time.sleep(1)
        await telegram_acc.send_message(
            chat_identifier=config["telegram_send_chat_identifier"],
            message_text=post["content"],
            media_gallery=post["media_gallery"]
        )
        with open(TELEGRAM_POSTS_FILE, "a") as telegram_posts_file:
            telegram_posts_file.write(f"{post['id']}\n")

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
        reddit_posts = await reddit.check_posts(config["reddit_filter"], config["reddit_limit"])
        # Se houver posts novos no Reddit, deve executar o passo de envio
        for post in reddit_posts:
            if TWITTER_SEND:
                await twitter_send_macro(post, twitter_post_list)
            if EMAIL_SEND:
                email_text=f"Olá,\n\nHá um novo post no Reddit."
                await mail_send_macro(subject=post["content"], text=email_text) 
            if TELEGRAM_SEND:
                await telegram_send_macro(post, telegram_post_list)

    if TELEGRAM_RECEIVE:
        print("oi")
        telegram_posts = await telegram_acc.collect_new_posts(config["telegram_receive_chat_identifier"], config["telegram_limit"])
        # Se houver posts novos no Telegram, deve executar o passo de envio
        print("Recebe do telegram")
        print(telegram_posts)
        for post in telegram_posts:
            if TWITTER_SEND:
                await twitter_send_macro(post, twitter_post_list)
            if EMAIL_SEND:
                email_text=f"Olá,\n\nHá um novo post no Telegram."
                await mail_send_macro(subject=post["author"], text=email_text)
    return


async def run():
    # Sua lógica de monitor
    await monitor()

async def main():
    while RUNNING:
        start_time = time.time()

        print("🔄 Iniciando rotina...")
        await run()
        print("✅ Rotina finalizada.")

        # Espera 600 segundos (10 minutos) a partir do término da rotina
        elapsed = time.time() - start_time
        wait_time = 600 - elapsed
        if wait_time > 0:
            print(f"⏳ Aguardando {int(wait_time)}s até a próxima execução.")
            await asyncio.sleep(wait_time)
        else:
            print("⚠️ A execução demorou mais que 600s. Iniciando próxima imediatamente.")

if __name__ == "__main__":
    asyncio.run(main())
