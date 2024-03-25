import copy
from database.database import users_id
from lexicon.lexicon import FIELD_SIZE,FIELD


def get_field_start(user_id: int) -> None:
    users_id[user_id]['field'] = FIELD


