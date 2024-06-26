LEXICON_WORK: dict = {
    'main_menu' : '<b><u><code>__________Главное меню__________</code></u></b>\n\n',
    'application' : '<b><u><code>____________Заявки____________</code></u></b>\n\n',
    'name_department' : '📩  Введите службу от которой поступила заявка<i>(Если её нет поставьте -)</i>',
    'name_house' : '🏠 Введите название здания,где будут выполняться работы <i>(Если его нет поставьте -)</i>',
    'number_cabinet' : '🔢 Введите номер кабинета <i>(Если его нет поставьте -)</i>',
    'what_to_do' : '⚙️ Введите, что нужно сделать',
    'full_application' : '<code>Вы завершили оформление.</code>',
    'save_application' : ' <b><code>✅ Заявка успешно добавлена.</code>\n</b>',
    'delete_application' : '🗑️ Заявка успешно удалена',
    'active_application' : '<b><u><code>________Действующие заявки________</code></u></b>',
    'completed_application' : '<b><u><code>________Выполненные заявки________</code></u></b>',
    'closing_app_count' : '🔢 Введите кол-во затраченного материала',
    'closing_add_material': 'Введите данные следующего формата: {name;union;count}.\nНапример: (Кабель ВВГнг 3х2,5;м;5)',
    'save_data_application' : '<code>Данные успешно сохранены, если хотите ещё что-то добавить перейдите в материалы,'
                              'если нет, то закройте заявку.</code>',
    'materials_other' : 'Введите название материала который был затрачен.',
    'count_other' : 'Введите сколько их было использовано.',
    'cancel_application' : '<b><u><code>________Отменённые заявки________</code></u></b>',
    'result_month' : '<b><u><code>________Выберите месяц________</code></u></b>',
    'choose_material': '<b><u>Выберите затраченные материалы</u></b>',
    'stock' : '<b><u><code>__________Склад__________</code></u></b>',
    'stock_add_column' : 'Ⓜ️ Введите полное название материала (Например: Кабель ВВГнг 3х2,5)',
    'stock_add_count' : '🔢 Введите кол-во данного материала',
    'add_del_stock' : '<code>Для добавления введённых данных используйте кнопку <i>➕ Добавить</i>\n'
                      'Для того чтобы отменить введёные данные используйте кнопку <i>❎ Отмена</i></code>',
    'add_stock' : '✅ Материал успешно добавлен.',
    'stock_add_unit' : '🔰 Введите единицу измерения (Например: шт, м и т.д.).',
    'cancel_stock': '🗑️ Данные были очищены.',
    'add_success' : '✅ Данные успешно обновлены.',
    'take_away_success' : '✅ Данные успешно обновлены.',
    'delete_stock' : '🗑️ Материал успешно удалён.',
    'sqlite3.OperationalError' : '❕ <b>Данный материал уже имеется в базе.</b>',
    'error_len_32' : '❗️ <b>Ошибка. Максимальная длина 30 символа. Попробуйте ещё раз.</b>',
    'purchase' : '<b><u><code>________Меню закупки________</code></u></b>',
    'p_application' : '<code>______Заявка на материалы______</code>',
    'p_materials_add' : 'Введите название материала,который хотите добавить в раздел <b>"Закупка материалов."</b>',
    'error_len_35' : '❗️ <b>Ошибка. Максимальная длина 35 символа. Попробуйте ещё раз.</b>',
    'echo' : '❕ <b>Вы не ввели данные. Попробуйте ещё раз или выйдите в <i>главное меню</i>.<b>',
    'delete_materials' : '<b>Нажмите на материал, который хотите удалить.</b>',
    'error_del' : '❕ Вам больше нечего удалять.',
    'p_to_50b': '<code>_________Несметка до 50б_________</code>',
    'p_to_50b_add': 'Введите название материала,который хотите добавить в раздел <b>"Несметка до 50 базовых."</b>',
    'p_over_50b': '<code>_________Несметка свыше 50б_________</code>',
    'p_over_50b_add': 'Введите название материала,который хотите добавить в раздел <b>"Несметка свыше 50 базовых."</b>',
    'enter_notes' : '<b>Введите заметку</b>',
    'library_main_menu': '<code>__________Библиотека__________</code>',
    'add_err' : '❕ <b>Данный материал уже добавлен</b>',
    'english_dict_not_correct_answer' : 'Это неверно, попробуйте ещё раз',
    'error_int' : '❕ <b>Нужно ввести число. Попробуйте ещё раз.</b>',
    'error_entry_name' : '❕ <b>Нужно ввести данные в формате {name;union;count}.\nНапример: (Кабель ВВГнг 3х2,5;м;5).</b>'

}

LEXICON_MAIN_MENU: dict = {
    '/main_menu' : 'Выйти в главное меню',
    '/en_ru_dict_simulator' : 'Тренажёр по англ-руск словам',
    '/ru_en_dict_simulator' : 'Тренажёр по руск-англ словам',
    '/english_dict' : 'Словарь по английскому',
    '/add_schedule' : 'Установить напоминание',
}

LEXICON_APPLICATION: dict = {
    '📝 Добавить заявку' : 'add_application',
    '⌛ Действующие заявки' : 'active_application',
    '✅ Выполненные заявки' : 'completed_application',
    '❎ Отменённые заявки' : 'cancel_application',
    '🟰 Итоги за месяц' : 'result_month',
    'Назад 🔙': 'back_main_menu'
}

LEXICON_MAIN_MENU_KB: dict = {
    '📩 Заявки' : 'application',
    '🏦 Склад' : 'stock',
    '💰 Закупка' : 'purchase',
    '📚 Библиотека' : 'library',
    '📞 Телефонный справочник МЭС' : 'phonebook',
}


LEXICON_RESULT_MONTH_KB: dict = {
    'Январь' : 'January',
    'Февраль': 'February',
    'Март': 'March',
    'Апрель': 'April',
    'Май': 'May',
    'Июнь': 'June',
    'Июль': 'July',
    'Август': 'August',
    'Сентябрь': 'September',
    'Октябрь': 'October',
    'Ноябрь': 'November',
    'Декабрь': 'December'
}

LEXICON_PHONEBOOK_SHORT: dict = {
    'short_list' : '<i>📞 Жаворонок Дмитрий Леонидович - <b>388</b>\n'
                   '📞 Головач Надежда Антоновна - <b>410</b>\n'
                   '📞 Абулхаиров Нурлан Утепкалиевич - <b>474</b>\n'
                   '📞 Федотова Алла Михайловна - <b>344</b>\n'
                   '📞 Галко Надежда Сергеевна - <b>303</b>\n'
                   '📞 Лихтарович Елена Викторовна - <b>480</b>\n'
                   '📞 Сашина Вера Михайловна - <b>321</b>\n'
                   '📞 Тригуб Татьяна Евгеньевна(буфет) - <b>301</b>'
                   '</i>'
}