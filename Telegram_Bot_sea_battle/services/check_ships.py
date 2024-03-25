from database.database import users_id,game_field_ships

def check_ships_all(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True

def check_ships_all_start(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True


def check_ships_straight(callback,callback_data):
    if  users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x-1][callback_data.y] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] == 1:
        return True

def check_ships_oblique(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
    users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
    users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True



def check_ships_straight_max_null(callback,callback_data):
    if callback_data.x == 0 and callback_data.y == 0:
        if users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] == 1:
            return True
    elif callback_data.x == 7 and callback_data.y == 7:
        if users_id[callback.from_user.id]['ships'][callback_data.x-1][callback_data.y] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] == 1:
            return True
    elif callback_data.x == 0 and callback_data.y == 7:
        if users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] == 1:
            return True
    elif callback_data.x == 7 and callback_data.y == 0:
        if users_id[callback.from_user.id]['ships'][callback_data.x-1][callback_data.y] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] == 1:
            return True
    elif callback_data.y == 7:
        if users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x-1][callback_data.y] == 1 or\
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] == 1:
            return True
    elif callback_data.y == 0:
        if users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x-1][callback_data.y] == 1 or\
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] == 1:
            return True
    elif callback_data.x == 7:
        if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] == 1 or\
                users_id[callback.from_user.id]['ships'][callback_data.x-1][callback_data.y] == 1:
            return True
    elif callback_data.x == 0:
        if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] == 1 or\
                users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] == 1:
            return True



def check_ships_oblique_max_null(callback,callback_data):
    if callback_data.x == 0 and callback_data.y == 0:
        if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y+1] == 1:
            return True
    elif callback_data.x == 0 and callback_data.y == 7:
        if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y-1] == 1:
            return True
    elif callback_data.x == 7 and callback_data.y == 7:
        if users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y-1] == 1:
            return True
    elif callback_data.x == 7 and callback_data.y == 0:
        if users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y+1] == 1:
            return True
    elif callback_data.x == 0:
        if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y-1] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y+1] == 1:
            return True
    elif callback_data.x == 7:
        if users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y-1] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y+1] == 1:
            return True
    elif callback_data.y == 0:
        if users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y + 1] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y+1] == 1:
            return True
    elif callback_data.y == 7:
        if users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y - 1] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y-1] == 1:
            return True
def check_ships_all_for_player_1(x,callback_data):
    if callback_data.x == 0 or callback_data.y == 0 or callback_data.x == 7 or callback_data.y == 7:
        if callback_data.x == 0 and callback_data.y == 0:
            if game_field_ships[x]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x][callback_data.y+1] == 1:
                return True
        elif callback_data.x == 7 and callback_data.y == 7:
            if game_field_ships[x]['ships'][callback_data.x-1][callback_data.y] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x][callback_data.y-1] == 1:
                return True
        elif callback_data.x == 0 and callback_data.y == 7:
            if game_field_ships[x]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x][callback_data.y-1] == 1:
                return True
        elif callback_data.x == 7 and callback_data.y == 0:
            if game_field_ships[x]['ships'][callback_data.x-1][callback_data.y] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x][callback_data.y+1] == 1:
                return True
        elif callback_data.y == 7:
            if game_field_ships[x]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x-1][callback_data.y] == 1 or\
                    game_field_ships[x]['ships'][callback_data.x][callback_data.y-1] == 1:
                return True
        elif callback_data.y == 0:
            if game_field_ships[x]['ships'][callback_data.x+1][callback_data.y] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x-1][callback_data.y] == 1 or\
                    game_field_ships[x]['ships'][callback_data.x][callback_data.y+1] == 1:
                return True
        elif callback_data.x == 7:
            if game_field_ships[x]['ships'][callback_data.x][callback_data.y+1] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x][callback_data.y-1] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x-1][callback_data.y] == 1:
                return True
        elif callback_data.x == 0:
            if game_field_ships[x]['ships'][callback_data.x][callback_data.y+1] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x][callback_data.y-1] == 1 or\
                    game_field_ships[x]['ships'][callback_data.x+1][callback_data.y] == 1:
                return True
        elif callback_data.x == 0 and callback_data.y == 0:
            if game_field_ships[x]['ships'][callback_data.x + 1][callback_data.y+1] == 1:
                return True
        elif callback_data.x == 0 and callback_data.y == 7:
            if game_field_ships[x]['ships'][callback_data.x + 1][callback_data.y-1] == 1:
                return True
        elif callback_data.x == 7 and callback_data.y == 7:
            if game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y-1] == 1:
                return True
        elif callback_data.x == 7 and callback_data.y == 0:
            if game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y+1] == 1:
                return True
        elif callback_data.x == 0:
            if game_field_ships[x]['ships'][callback_data.x + 1][callback_data.y-1] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x + 1][callback_data.y+1] == 1:
                return True
        elif callback_data.x == 7:
            if game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y-1] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y+1] == 1:
                return True
        elif callback_data.y == 0:
            if game_field_ships[x]['ships'][callback_data.x+1][callback_data.y + 1] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y+1] == 1:
                return True
        elif callback_data.y == 7:
            if game_field_ships[x]['ships'][callback_data.x+1][callback_data.y - 1] == 1 or \
                    game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y-1] == 1:
                return True

    else:
        if game_field_ships[x]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
                game_field_ships[x]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
                game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
                game_field_ships[x]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
                game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
                game_field_ships[x]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
                game_field_ships[x]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
                game_field_ships[x]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
            return True


def check_ships_all_new_horizontally(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 2] == 1:
        return True
def check_ships_all_new_horizontally_6(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 2] == 1:
        return True
def check_ships_all_new_horizontally_1(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_horizontally_7(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 2] == 1:
        return True
def check_ships_all_new_horizontally_0(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 2] == 1:
        return True

def check_ships_all_new_vertically_1(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 2][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 2][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_vertically_6(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_vertically_7(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_vertically_0(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y ] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1:
        return True

def check_ships_all_new_vertically(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 2][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 2][callback_data.y - 1] == 1:
        return True



def check_ships_all_new_horizontally_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_horizontally_6_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_horizontally_1_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 2] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_horizontally_7_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_horizontally_0_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True

def check_ships_all_new_vertically_1_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_vertically_6_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_vertically_7_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y-1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True
def check_ships_all_new_vertically_0_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y ] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y+1] == 1:
        return True

def check_ships_all_new_vertically_two(callback,callback_data):
    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x - 2][callback_data.y - 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1:
        return True

def check_cells_on_availability_ships(callback_data):
    if callback_data.x == 0 and callback_data.y == 0:
        if game_field_ships[1]['field'][callback_data.x + 1][callback_data.y] == 3:
            game_field_ships[1]['field'][callback_data.x + 1][callback_data.y] = 2
        if game_field_ships[1]['field'][callback_data.x][callback_data.y + 1] == 3:
            game_field_ships[1]['field'][callback_data.x][callback_data.y + 1] = 2
        if game_field_ships[1]['field'][callback_data.x + 2][callback_data.y] == 3:
            game_field_ships[1]['field'][callback_data.x + 2][callback_data.y] = 2
        if game_field_ships[1]['field'][callback_data.x][callback_data.y + 2] == 3:
            game_field_ships[1]['field'][callback_data.x][callback_data.y + 2] = 2
    elif callback_data.x == 0 and callback_data.y == 7:
        if game_field_ships[1]['field'][callback_data.x + 1][callback_data.y] == 3:
            game_field_ships[1]['field'][callback_data.x + 1][callback_data.y] = 2
        if game_field_ships[1]['field'][callback_data.x][callback_data.y - 1] == 3:
            game_field_ships[1]['field'][callback_data.x][callback_data.y - 1] = 2
        if game_field_ships[1]['field'][callback_data.x + 2][callback_data.y] == 3:
            game_field_ships[1]['field'][callback_data.x + 2][callback_data.y] = 2
        if game_field_ships[1]['field'][callback_data.x][callback_data.y - 2] == 3:
            game_field_ships[1]['field'][callback_data.x][callback_data.y - 2] = 2
    elif callback_data.x == 7 and callback_data.y == 0:
        if game_field_ships[1]['field'][callback_data.x - 1][callback_data.y] == 3:
            game_field_ships[1]['field'][callback_data.x - 1][callback_data.y] = 2
        if game_field_ships[1]['field'][callback_data.x][callback_data.y + 1] == 3:
            game_field_ships[1]['field'][callback_data.x][callback_data.y + 1] = 2
        if game_field_ships[1]['field'][callback_data.x - 2][callback_data.y] == 3:
            game_field_ships[1]['field'][callback_data.x - 2][callback_data.y] = 2
        if game_field_ships[1]['field'][callback_data.x][callback_data.y + 2] == 3:
            game_field_ships[1]['field'][callback_data.x][callback_data.y + 2] = 2
    elif callback_data.x == 7 and callback_data.y == 7:
        if game_field_ships[1]['field'][callback_data.x - 1][callback_data.y] == 3:
            game_field_ships[1]['field'][callback_data.x - 1][callback_data.y] = 2
        if game_field_ships[1]['field'][callback_data.x][callback_data.y - 1] == 3:
            game_field_ships[1]['field'][callback_data.x][callback_data.y - 1] = 2
        if game_field_ships[1]['field'][callback_data.x - 2][callback_data.y] == 3:
            game_field_ships[1]['field'][callback_data.x - 2][callback_data.y] = 2
        if game_field_ships[1]['field'][callback_data.x][callback_data.y - 2] == 3:
            game_field_ships[1]['field'][callback_data.x][callback_data.y - 2] = 2
    elif callback_data.x == 0:
        if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
        if game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] = 2
    elif callback_data.x == 7:
        if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
        if game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] = 2
    elif callback_data.y == 0:
        if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
        if game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
    elif callback_data.y == 7:
        if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
        if game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] == 3:
            game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
        if game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] == 3:
            game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] = 2
    else:
        try:
            if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
                game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
            if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
                game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] = 2
            if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
                game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
            if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
                game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
            if game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] == 3:
                game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
            if game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] == 3:
                game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] = 2
            if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
                game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
            if game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] == 3:
                game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] = 2
        except IndexError:
            if callback_data.x == 1:
                if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
                if game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] = 2
            elif callback_data.x == 6:
                if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
                if game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] = 2
            elif callback_data.y == 1:
                if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
                if game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
            elif callback_data.y == 6:
                if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
                if game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] = 2
            else:
                if game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x + 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 1][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 1] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 1] = 2
                if game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x + 2][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] == 3:
                    game_field_ships[2]['field'][callback_data.x - 2][callback_data.y] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y + 2] = 2
                if game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] == 3:
                    game_field_ships[2]['field'][callback_data.x][callback_data.y - 2] = 2
