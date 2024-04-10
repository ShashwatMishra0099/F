from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Replace these placeholders with your values
BOT_TOKEN = '6811749953:AAGdD19D6gJBAhyIATWKIai4S23so3BHXBc'
GROUP_ID = '-1002010714711'

# Define states for the conversation handler
USERNAME, ACCESS_HASH, USER_ID = range(3)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Welcome! Please provide the username of the member you want to add:"
    )
    return USERNAME

def username(update: Update, context: CallbackContext) -> int:
    context.user_data['username'] = update.message.text
    update.message.reply_text(
        "Great! Now, please provide the access hash of the member:"
    )
    return ACCESS_HASH

def access_hash(update: Update, context: CallbackContext) -> int:
    context.user_data['access_hash'] = update.message.text
    update.message.reply_text(
        "Excellent! Finally, please provide the user ID of the member:"
    )
    return USER_ID

def user_id(update: Update, context: CallbackContext) -> None:
    # Check if the 'user_id' key exists in context.user_data
    if 'user_id' not in context.user_data:
        update.message.reply_text("Oops! Something went wrong. Please start the conversation again.")
        return ConversationHandler.END

    # Get the provided username, access hash, and user ID
    username = context.user_data['username']
    access_hash = context.user_data['access_hash']
    user_id = context.user_data['user_id']

    try:
        # Add member to the group
        context.bot.add_chat_member(chat_id=GROUP_ID, user_id=user_id, access_hash=access_hash)
        update.message.reply_text(f"{username} added successfully to the group!")
    except Exception as e:
        update.message.reply_text(f"Error adding {username} to the group: {e}")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Operation cancelled."
    )
    return ConversationHandler.END

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, username)],
            ACCESS_HASH: [MessageHandler(Filters.text & ~Filters.command, access_hash)],
            USER_ID: [MessageHandler(Filters.text & ~Filters.command, user_id)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
