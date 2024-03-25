from aiogram.filters.state import State,StatesGroup

class FSMWork(StatesGroup):
    main_menu = State()
    application = State()
    completed_application = State()
    cancel_application = State()
    add_application = State()
    name_department = State()
    name_house = State()
    number_cabinet = State()
    what_to_do = State()
    save_delete_application = State()
    result_month = State()
    result_month_press = State()
    notes = State()
    english_dict_simulator = State()
    ru_en_dict_simulator = State()
    english_dict = State()

class FSMCloseApplication(StatesGroup):
    close_application = State()
    delete_application = State()
    cable = State()
    sockets = State()
    cable_channel = State()
    automatic_switch = State()
    diff_automatic = State()
    mounting_boxes = State()
    switch = State()
    lightbulbs = State()
    other = State()
    save_data_application = State()
    internal_sockets = State()
    external_sockets = State()
    a_single_phase_kb = State()
    a_triple_phase_kb = State()
    d_single_phase_kb = State()
    d_triple_phase_kb = State()
    internal_switch = State()
    external_switch = State()
    other_count = State()
    close_or_continue_kb = State()

    entry_count = State()
    entry_name = State()

class FSMWork_stock(StatesGroup):
    main_menu = State()
    add_column = State()
    add_count = State()
    add_unit = State()
    press_add_count = State()
    press_take_away_count = State()


class FSMWork_purchase(StatesGroup):
    main_menu = State()
    materials_add = State()
    to_50b_add = State()
    over_50b_add = State()

class FSMWork_library(StatesGroup):
    main_menu = State()

class FSMWork_phonebook(StatesGroup):
    main_menu = State()

class FSMWork_schedule(StatesGroup):
    send_date = State()
    send_text = State()