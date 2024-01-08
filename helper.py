def is_price(s):
    try:
        float(s)
        return float(s) >= 0
    except ValueError:
        return False

def is_number(s):
    try:
        int(s)
        return int(s) >= 0
    except ValueError:
        return False

        
def equal(first_amt, second_amt):
    return abs(first_amt - second_amt) <= 0.01


def additem_parse(user_input):
    remove_command = user_input[9:]
    user_args = remove_command.split(' ', 1)
    if len(user_args) != 2:
        return None
    
    item_price = user_args[0]
    item_name = user_args[1]

    if not is_price(item_price):
        return None

    return [item_price, item_name]

def condense_expenses(list_of_users, list_of_items):
    list_of_contributions = []
    for user in list_of_users:
        contribution = [user[0], 0]
        for item in list_of_items:
            if item[1] == user[0]:
                contribution[1] += item[3]
        list_of_contributions.append(contribution)
    
    return list_of_contributions


def split(members):
    # find total paid
    total = 0
    for member in members:
        total += member[1]

    # find average amount per person
    avg = total / len(members)
    # split members into 2 groups
    to_pay = []
    to_recieve = []
    for member in members:
        if equal(member[1],avg):
            continue
        elif member[1] < avg:
            to_pay.append([member[0], avg - member[1]])
        elif member[1] > avg:
            to_recieve.append([member[0], member[1] - avg])
    # go through the list of people to pay, pay required amount to people to recieve
    payer_index = 0
    reciever_index = 0
    transactions = []
    while payer_index < len(to_pay) and reciever_index < len(to_recieve):
        curr_payer = to_pay[payer_index]
        curr_reciever = to_recieve[reciever_index]

        if equal(curr_payer[1], curr_reciever[1]):
            transactions.append([curr_payer[0], curr_reciever[0], curr_reciever[1]])
            payer_index += 1
            reciever_index += 1
        elif curr_payer[1] > curr_reciever[1]:
            transactions.append([curr_payer[0], curr_reciever[0], curr_reciever[1]])
            curr_payer[1] -= curr_reciever[1]
            reciever_index += 1

        elif curr_payer[1] < curr_reciever[1]:
            transactions.append([curr_payer[0], curr_reciever[0], curr_payer[1]])
            curr_reciever[1] -= curr_payer[1]
            payer_index += 1
    return transactions