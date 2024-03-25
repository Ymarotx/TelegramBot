users_id: dict[int, dict[str,list]] = {}
user_ships: dict[int, dict[str,int]] = {}
user_press_three_two_one: dict[int, dict[int,int]] = {}
players_id: dict[str,int] = {}
game_field_ships: dict[int, dict[str,list]] = {}
game_field_ships_name_players: dict[int,str] = {}
game_field_ships_id_players: dict[int,int] = {}
game_message_id_field_user: list[int] = [] #0 - second player,1 - first player
message_id_delete: dict[str,int] = {}
state_wait: dict[int,bool] = {} #True - ожидает , False - нет
user_id_win: dict[int,list[str]] = {}
user_state: dict[int,str] = {}



