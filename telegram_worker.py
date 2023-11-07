import keys
from detoxify import Detoxify
from db_model import db_conn
from telegram.constants import ParseMode
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from telegram.ext import (Application, CommandHandler,
                          filters, MessageHandler)


class Detox:
    encoder_max_len = 42
    decoder_max_len = 42

    def __init__(self) -> None:
        # Detoxifier tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

        # Detoxifier model
        self.model = AutoModelForSeq2SeqLM.from_pretrained("models/")

        import torch
        self.device = torch.device(
            "cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.model.to(self.device)

    def text_convertion(self, comment):

        input_ids = self.tokenizer(comment, return_tensors="pt", padding='max_length',
                                   truncation=True, max_length=300).input_ids
        outputs = self.model.generate(
            input_ids.to(self.device), max_length=400)
        converted_text = self.tokenizer.decode(
            outputs[0], max_length=400, skip_special_tokens=True)
        converted_text = converted_text.replace("non-toxic ", "")
        converted_text = converted_text.replace(".", " \.")
        return converted_text

async def start_comment(update, context):
    await update.message.reply_text("Hello there!!!, Lets begin!")


async def message_handler_function(update, context):

    text_message = update.message.text
    result = toxicity_check_model.predict(text_message)
    if result.get('toxicity') > 0.4:
        await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)

        chat_id = update.effective_chat.id
        date = update.message.date
        username = update.message.from_user.username
        detox_version = detox_model.text_convertion(text_message)
        user = f"User {username} sent a toxic message\. "
        non_toxic = f"Detoxified version: {detox_version}\."

        row = db.add_row({
            "toxic_text": text_message,
            "neutered_text": detox_version.replace(' \.','.'),
            "sender": username,
            "incident_date": date
        })

        text_message = text_message.replace(".", " \.")
        toxic_version = f"Toxic version:  ||{text_message}||"

        # Format the message as a spoiler using Markdown
        formatted_message = f"{user}\n{non_toxic}\n{toxic_version}"

        try:
            # Send the message with Markdown parsing mode
            await context.bot.send_message(chat_id=chat_id, text=formatted_message, parse_mode=ParseMode.MARKDOWN_V2)
            
        except Exception as e:
            formatted_message = f"{user}\n{toxic_version}"
            await context.bot.send_message(chat_id=chat_id, text=formatted_message, parse_mode=ParseMode.MARKDOWN_V2)
            print("Could not format string")
            print(e)
        await row
        
async def error(update, context):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print("Loading up model.....")
    toxicity_check_model = Detoxify('original')

    detox_model = Detox()

    application = Application.builder().token(keys.token).build()
    print("Loading DB")
    db = db_conn()
    print("Up and running")

    application.add_handler(CommandHandler('start', start_comment))
    application.add_handler(MessageHandler(
        filters.TEXT, message_handler_function,))

    application.add_error_handler(error)

    application.run_polling()
