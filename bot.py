from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters
from helper import split, additem_parse, condense_expenses, is_number
from model import is_session_ongoing, start_session, is_user_in_session, add_user_to_session, delete_user_from_session, get_users_in_session, add_item_to_session, get_items_in_session, delete_item_from_session, end_session

WELCOME_MESSAGE = """Hello there! Planning parties can be tiresome and tedious. Someone needs to book the venue, another person needs to buy food while someone else buys the drinks etc.

I can help you keep track of the expenses while planning your party! After you've finished the party, I can help calculate who to pay how much to who so that everyone contributes equally to the party!

<b>To manage users:</b>
/adduser - to add yourself to the party
/listuser - to list everyone who came
/deleteuser - to remove yourself from the party

<b>To manage items:</b>
/additem [item_price] [item_name] - to add an item to the party
/deleteitem - to delete an item from the party
/listitems - to list all items in their party

/finish - to stop adding people and items to the party"""

ONGOING_SESSION_MESSAGE = 'You have already started a session'

SESSION_NOT_STARTED_MESSAGE = 'You have not started a session. Send /start first.'

USER_ALREADY_ADDED_MESSAGE = 'You have already added yourself to the party.'

USER_NOT_ADDED_MESSAGE = 'You have not added yourself to the party, use\n\n/adduser\n\nif you wish to add yourself to the party.'

NO_USER_IN_SESSION_MESSAGE = 'No one has been added, use\n\n/adduser\n\nif you wish to add yourself to the party.'

INDEX_STAGE = 1

def send_error(update, context, message):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    return


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if is_session_ongoing(chat_id):
        send_error(update, context, ONGOING_SESSION_MESSAGE)
        return
    
    start_session(chat_id)
    context.bot.send_message(chat_id=chat_id, text=WELCOME_MESSAGE, parse_mode='html')


def finish(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if not is_session_ongoing(chat_id):
        send_error(update, context, SESSION_NOT_STARTED_MESSAGE)
        return

    list_of_users = get_users_in_session(chat_id)
    list_of_items = get_items_in_session(chat_id)

    if not list_of_users:
        context.bot.send_message(chat_id=chat_id, text='No one came to this party')
    elif not list_of_items:
        context.bot.send_message(chat_id=chat_id, text='No items have been added to this party')
    else:        
        list_of_contributions = condense_expenses(list_of_users, list_of_items)
        transactions = split(list_of_contributions)

        message = 'Pay up:\n'

        for transaction in transactions:
            message += transaction[0] + ' pay ' + transaction[1] + ' $' + str(round(transaction[2], 2)) + '\n'
        context.bot.send_message(chat_id=chat_id, text=message)
    end_session(chat_id)


def add_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    username = update.message.from_user.username

    if not is_session_ongoing(chat_id):
        send_error(update, context, SESSION_NOT_STARTED_MESSAGE)
        return

    if is_user_in_session(chat_id, username):
        send_error(update, context, USER_ALREADY_ADDED_MESSAGE)
        return

    add_user_to_session(chat_id, username)
    list_of_users = get_users_in_session(chat_id)
    update.message.reply_text('Number of people in this party: ' + str(len(list_of_users)))


def list_users(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if not is_session_ongoing(chat_id):
        send_error(update, context, SESSION_NOT_STARTED_MESSAGE)
        return

    list_of_users = get_users_in_session(chat_id)

    if not list_of_users:
        send_error(update, context, NO_USER_IN_SESSION_MESSAGE)
        return

    message = 'Listing everyone who came:\n'

    for user in list_of_users:
        message += user[0] + '\n'
    update.message.reply_text(message)


def delete_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    username = update.message.from_user.username

    if not is_session_ongoing(chat_id):
        send_error(update, context, SESSION_NOT_STARTED_MESSAGE)
        return

    if not is_user_in_session(chat_id, username):
        send_error(update, context, USER_NOT_ADDED_MESSAGE)
        return

    delete_user_from_session(chat_id, username)
    list_of_users = get_users_in_session(chat_id)
    update.message.reply_text('Number of people in this party: ' + str(len(list_of_users)))


def add_item(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    username = update.message.from_user.username
    user_input = update.message.text

    if not is_session_ongoing(chat_id):
        send_error(update, context, SESSION_NOT_STARTED_MESSAGE)
        return

    if not is_user_in_session(chat_id, username):
        send_error(update, context, USER_NOT_ADDED_MESSAGE)
        return
    
    new_item = additem_parse(user_input)

    if not new_item:
        send_error(update, context, 'USAGE:\n\n/additem [item_price] [item_name]\n\n[item_price] must be a non-negative number without dollar sign')
        return

    add_item_to_session(chat_id, username, new_item[1], new_item[0])
    list_of_items = get_items_in_session(chat_id)
    update.message.reply_text('Number of items in this party: ' + str(len(list_of_items)))


def list_items(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if not is_session_ongoing(chat_id):
        send_error(update, context, SESSION_NOT_STARTED_MESSAGE)
        return
    
    list_of_items = get_items_in_session(chat_id)

    if not list_of_items:
        send_error(update, context, 'No items in this party yet, use \n\n/additem [item_price] [item_name]\n\nto add items')
        return

    message = 'Listing all items:\n'

    for index, item in enumerate(list_of_items):
        message += str(index + 1) + '. ' + item[1] + ' bought ' + item[2] + ' for $' + str(round(item[3], 2)) + '\n'
    update.message.reply_text(message)
    return
    

def list_items_for_convo(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    username = update.message.from_user.username
    user_input = update.message.text

    if not is_session_ongoing(chat_id):
        send_error(update, context, SESSION_NOT_STARTED_MESSAGE)
        return ConversationHandler.END

    if not is_user_in_session(chat_id, username):
        send_error(update, context, USER_NOT_ADDED_MESSAGE)
        return ConversationHandler.END
    
    list_of_items = get_items_in_session(chat_id)

    if not list_of_items:
        send_error(update, context, 'No items in this party yet, use \n\n/additem [item_price] [item_name]\n\nto add items')
        return ConversationHandler.END

    message = 'Please send the index number for the item you want to delete:\n'

    for index, item in enumerate(list_of_items):
        message += str(index + 1) + '. ' + item[1] + ' | ' + item[2] + ' | $' + str(round(item[3], 2)) + '\n'
    
    message += '\n/cancel to cancel this operation'
    update.message.reply_text(message)
    return INDEX_STAGE


def delete_item(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    username = update.message.from_user.username
    user_input = update.message.text

    if not is_number(user_input):
        send_error(update, context, 'Please send a number only')
        return INDEX_STAGE

    index = int(user_input) - 1
    list_of_items = get_items_in_session(chat_id)

    if index < 0 or index >= len(list_of_items):
        send_error(update, context, 'Please send a valid index')
        return INDEX_STAGE

    item_to_delete = list_of_items[index]
    item_to_delete_id = item_to_delete[0]
    delete_item_from_session(chat_id, item_to_delete_id)
    update.message.reply_text(item_to_delete[2] + ' has been deleted')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    send_error(update, context, 'The operation has been cancelled')
    return ConversationHandler.END

token_file = open("token.txt", "r")
token = token_file.read()
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
finish_handler = CommandHandler('finish', finish)

adduser_handler = CommandHandler('adduser', add_user)
listusers_handler = CommandHandler('listuser', list_users)
deleteuser_handler = CommandHandler('deleteuser', delete_user)

additem_handler = CommandHandler('additem', add_item)
listitems_handler = CommandHandler('listitems', list_items)
deleteitem_handler = ConversationHandler(
    entry_points=[CommandHandler('deleteitem', list_items_for_convo)],
    states={
        INDEX_STAGE: [
            CommandHandler('cancel', cancel),
            MessageHandler(Filters.text, delete_item)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(finish_handler)
dispatcher.add_handler(adduser_handler)
dispatcher.add_handler(listusers_handler)
dispatcher.add_handler(deleteuser_handler)

dispatcher.add_handler(additem_handler)
dispatcher.add_handler(listitems_handler)
dispatcher.add_handler(deleteitem_handler)

updater.start_polling()

updater.idle()