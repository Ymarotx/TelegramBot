from database.database import game_field_ships_id_players

def choose_id(id: int):
    if game_field_ships_id_players[1] == id:
        return game_field_ships_id_players[2]
    else:
        return game_field_ships_id_players[1]

