This Telegram bot converts .epub files to .kepub.epub format using the Kepubify software. It supports files up to 20MB in size, as limited by the Telegram API.

If you want to make your own bot, follow these steps:   
1. Download Kepubify from https://pgaskin.net/kepubify and place the binary in the `src` folder of this project.  
2. Create a new bot on Telegram by talking to the BotFather (https://t.me/botfather) and get your bot token.  
3. Set the bot token as an environment variable named `TELEGRAM_API_TOKEN`. 
4. Install the dependencie: `python-telegram-bot`.  
5. Run the bot.

Alternatively, you can deploy the bot using Docker. You can build the Docker image with the provided Dockerfile and run it, ensuring to set the TELEGRAM_API_TOKEN environment variable with your bot token.