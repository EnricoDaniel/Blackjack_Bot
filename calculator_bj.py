import log

def decision(valuePlayer, valueDealer, remarkPlayer):
    if valueDealer == "a":
        valueDealer = 99
    if not remarkPlayer:
        action = hard_cards(valuePlayer, valueDealer)
    else:
        action = soft_cards(valuePlayer, valueDealer, remarkPlayer)
    return action

#i know this is spaghetti but i was kinda hyped for this project so i just went with it
#i actually pretend to update this method someday
def hard_cards(valuePlayer, valueDealer):
    if valuePlayer in range(4,8):
        action = "Hit"
    elif valuePlayer == 9:
        if valueDealer in range(3,6):
            action = "Double if possible, otherwise Hit"
        else:
            action = "Hit"
    elif valuePlayer == 10:
        if valueDealer in range(2,9):
            action = "Double if possible, otherwise Hit"
        else:
            action = "Hit"
    elif valuePlayer == 11:
        if valueDealer in range(2,10):
            action = "Double if possible, otherwise Hit"
        else:
            action = "Hit"
    elif valuePlayer == 12:
        if valueDealer in range(4,6):
            action = "Stand"
        else:
            action = "Hit"
    elif valuePlayer == 13 or valuePlayer == 14 or valuePlayer == 15:
        if valueDealer in range(2,6):
            action = "Stand"
        else:
            if valuePlayer == 15 and valueDealer == 10:
                action = "Surrender if possible, otherwise Hit"
            else:
                action = "Hit"
    elif valuePlayer == 16:
        if valueDealer in range(2,6):
            action = "Stand"
        else:
            if valueDealer in range(9,11):
                action = "Surrender if possible, otherwise Hit"
            else:
                action = "Hit"
    else:
        action = "Stand"
    log.logQueue("Jogador:" + str(valuePlayer))
    log.logQueue("Mesa:" + str(valueDealer))
    return action
        
def soft_cards(valuePlayer, valueDealer, remarkPlayer):
    valueAux = valuePlayer
    for eachRemark in remarkPlayer:
        valueAux = valueAux + 11
        if valueAux > 21:
            valueAux = valueAux - 11
            valueAux = valueAux + 1
    valuePlayer = valueAux
    if valuePlayer in range(13,17):
        if valueDealer in range(5,6):
            action = "Double if possible, otherwise Hit"
        elif valueDealer == 4:
            if valuePlayer in range(15,16):
                action = "Double if possible, otherwise Hit"
        elif valueDealer == 3:
            if valuePlayer == 17:
                action = "Double if possible, otherwise Hit"
        else:
            action = "Hit"
    elif valuePlayer == 18:
        if valueDealer in range(5,6):
            action = "Double if possible, otherwise Stand"
        elif valueDealer in range(9,11):
            action = "Hit"
        else:
            action = "Stand"
    else:
        action = "Stand"
    log.logQueue("Jogador:" + str(valuePlayer))
    log.logQueue("Mesa:" + str(valueDealer))
    return action
    