from aiogram.fsm.state import StatesGroup, State


class FSMMainMenu(StatesGroup):
    main_menu = State()
    dict = State()
    simulator = State()
    dict_all = State()
    simulator_new = State()
    end_simulator = State()

class FSMSimulator(StatesGroup):
    simulator_new = State()
    simulator_end = State()
