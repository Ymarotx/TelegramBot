from aiogram.filters.state import State,StatesGroup

class FSM_RP_TP(StatesGroup):
    start = State()
    give_access = State()
    deny_access = State()
    main_menu = State()
    name_rp_mres = State()
    location_rp_mres = State()
    name_tp_mres = State()
    location_tp_mres = State()

    name_rp_zres = State()
    location_rp_zres = State()
    name_tp_zres = State()
    location_tp_zres = State()

    name_rp_pres = State()
    location_rp_pres = State()
    name_tp_pres = State()
    location_tp_pres = State()

    name_rp_ogres = State()
    location_rp_ogres = State()
    name_tp_ogres = State()
    location_tp_ogres = State()