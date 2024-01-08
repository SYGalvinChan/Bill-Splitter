# Bill Splitter
## Description
Bill Splitter is a telegram bot designed to assist in settling the finance of small scale gathering.
When planning parties or gatherings, we will need to settle some expenses such as venue, food, drink etc.
Different people might have pay different amount for the various expenses.

## Running the Bot
1. Open Telegram
1. Search of `@BotFather`
1. Click `start` and select `/newbot`
1. Follow instructions to get a token
1. Create a new file `token.txt` in this directory and paste the token
1. Run `py bot.py`

## Usage
Use this bot to add the individual contributions you've made to the party. 
After the party, the bot will calculate who to pay how much to who.

## Commands

- `/start` - start a session

- `/adduser` - add a user to the session
- `/deleteuser` - delete a user in the session
- `/listuser` - list all users in the session

- `/additem` - add an item into the expense tracker | usage: `/additem [item_price] [item_name]`
- `/deleteitem` - delete an item in the expense tracker
- `/listitems` - list all items in the expense tracker

- `/finish` - split total expenses equally among all users in the session