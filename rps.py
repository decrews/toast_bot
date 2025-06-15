valid_selections = ["rock", "paper", "scissors"]

def initialize_rps(bot):
    bot.first_pick_name = None
    bot.first_pick_selection = None

def calc_rps(s1, s2):
    if (s1 == "rock" and s2 == "scissors"):
        return 0
    elif (s1 == "paper" and s2 == "rock"):
        return 0
    elif (s1 == "scissors" and s2 == "paper"):
        return 0
    return 1

def play_rps(bot, selection: str, name: str):
    if (selection in valid_selections):
        if (selection != None and bot.first_pick_selection == None):
            bot.first_pick_selection = selection
            bot.first_pick_name = name
            return f'{name} has started Rock, Paper Scissors'
        
        elif (selection != None and bot.first_pick_selection != None):
            result = calc_rps(bot.first_pick_selection, selection)
            result_string = f'{bot.first_pick_name}: {bot.first_pick_selection}\n{name}: {selection}\n{bot.first_pick_name if result == 0 else name} wins!'
            initialize_rps(bot)
            return result_string
    else:
        return "Not a valid selection! Gotta pick rock, paper, or scissors"