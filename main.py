import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with the token you obtained from BotFather
TOKEN = '6976204025:AAEAnnsQXuzkB8UGy_MQ84e4n8AMcb-rOak'

# Dictionary to store user-specific song lists
user_song_lists = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_song_lists:
        user_song_lists[user_id] = ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5"]
    update.message.reply_text('Welcome to the Karaoke Bot! Tap on the buttons below:', reply_markup=get_keyboard())

def sing(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_songs = user_song_lists.get(user_id, [])

    if not user_songs:
        update.message.reply_text("All songs have been sung. Add more songs!")
        return

    random_song = random.choice(user_songs)
    user_songs.remove(random_song)

    update.message.reply_text(f"Sing this karaoke song: {random_song}", reply_markup=get_keyboard())

def addsong(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    # Check if the user has a song list, if not, create one
    if user_id not in user_song_lists:
        user_song_lists[user_id] = []

    # Get the song added by the user
    user_input = context.args
    if not user_input:
        update.message.reply_text("Please provide a song to add. Usage: /addsong <song>")
        return

    song_to_add = ' '.join(user_input)

    # Add the song to the user's list
    user_song_lists[user_id].append(song_to_add)

    update.message.reply_text(f"Song '{song_to_add}' added to your list!", reply_markup=get_keyboard())

def get_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Sing a Song 🎤", callback_data='sing')],
        [InlineKeyboardButton("Add a Song 🎵", callback_data='addsong')],
    ]
    return InlineKeyboardMarkup(keyboard)

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'sing':
        sing(update, context)
    elif query.data == 'addsong':
        addsong(update, context)

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sing", sing))
    dp.add_handler(CommandHandler("addsong", addsong, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start))  # Handle text messages as if it's a /start command
    dp.add_handler(MessageHandler(Filters.regex('^Sing a Song 🎤$') | Filters.regex('^Add a Song 🎵$'), button_handler))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
