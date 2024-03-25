from aiogram.filters.state import State,StatesGroup



class FSMFillShipsGame(StatesGroup):
    admin = State()
    main_menu = State()
    choose_ships = State()
    set_ships_three_deck = State()
    set_ships_two_deck = State()
    set_ships_one_deck = State()
    find_opponent = State()
    main_menu_kb = State()
    wait_opponent = State()
    player_1 = State()
    three_view_horizontally = State()
    three_view_vertically = State()
    two_view_horizontally = State()
    two_view_vertically = State()





