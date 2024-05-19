from aiogram.fsm.state import StatesGroup, State


class FSMMainMenu(StatesGroup):
    main_menu = State()
    dict = State()
    simulator = State()
    dict_all = State()
    end_simulator = State()
    reminder = State()
    add_word = State()

class FSMSimulator(StatesGroup):
    simulator_new = State()
    simulator_end = State()
    simulator_new_end = State()

class FSMReminder(StatesGroup):
    get_time = State()
