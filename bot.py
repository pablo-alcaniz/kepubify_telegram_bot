import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

#### BOT CONF ####

# FUNCTIONS
def remove_par(input_str):
    return re.sub(r'[()[\]{}]','', input_str)

def remove_space(input_str):
    return re.sub(r'\s+','', input_str)

# GENERAL CONF
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BINARY_NAME = "kepubify"

# TOKEN CONF
TOKEN_PATH = os.path.join(BASE_DIR, 'TELEGRAM_API_TOKEN')

try: 
    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        TOKEN = f.read().strip()
except FileNotFoundError:
    raise ValueError(f"Token file not found in {TOKEN_PATH}")

#### BOT FUNCTIONS ####

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the (non oficial) Kepubify bot!")

async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send a .epub file and I will send you back a .kepub file!")

async def credits(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("-Please, visit the page of the author of the programm KEPUBIFY. https://pgaskin.net/kepubify \n -Bot made by Pablo Alcañiz (https://github.com/pablo-alcaniz/kepubify_telegram_bot)")

async def privacy(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("All the files that you send to us are deleted the moment after the converted file is delivered to you.")

async def handle_document(update: Update, context: CallbackContext) -> None:
    file = update.message.document
    if not file.file_name.endswith(".epub"):
        await update.message.reply_text("Please, send me only .epub docs.")
        return
    
    file_path = remove_space(remove_par(os.path.join(BASE_DIR, file.file_name)))
    new_file = await context.bot.get_file(file.file_id)
    await new_file.download_to_drive(file_path)

    output_file = remove_par(os.path.join(BASE_DIR, file.file_name.replace(".epub", ".kepub.epub")))
    command = BASE_DIR+"/"+BINARY_NAME+" "+str(file_path)+" -o "+str(output_file)

    try:
        os.system(command)
        await update.message.reply_document(document=open(output_file, "rb"), filename=os.path.basename(output_file))
    except:
        await update.message.reply_text("There was an unknown error.")

    os.remove(file_path)
    os.remove(output_file)


#### BOT EXECUTION ####

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("credits", credits))
    app.add_handler(CommandHandler("privacy", privacy))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    app.run_polling()

if __name__ == "__main__":
    main()


