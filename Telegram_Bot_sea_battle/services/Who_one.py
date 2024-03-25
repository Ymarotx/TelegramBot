import random


def who_one(player_1,player_2 : str):
    players_1 = random.randint(0,100)
    players_2 = random.randint(0,100)
    if players_1 == players_2:
        who_one(player_1,player_2)
    elif players_1 > players_2:
        return players_1,players_2,player_1
    else:
        return players_1,players_2,player_2



