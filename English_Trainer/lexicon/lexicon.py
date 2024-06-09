LEXICON_MAIN: dict[str,str] = {
    'main_menu' : '<b>_____________Главное меню_____________</b>',
    'dict' : '<b>_____________Словари_____________</b>',
    'simulator' : '<b>_____________Тренажёры_____________</b>',
    'add_word' : '<code>Введите слово для добавления. Для выхода используйте команду /main_menu.</code>',
    'add_word_err' : '<code>Для добавления слова вы должны быть в главном меню. Для выхода в главное меню используйте /main_menu.</code>'
}

LEXICON_SIMULATOR: dict[str,str] = {
    'simulator_exit' : '<code>Если вы выйдите из симулятора, ваш результат будет потерян. Используйте /main_menu после исчезновения этого окна, чтобы выйти.</code>',
    'simulator_last_page' : 'Вы уже находитесь на последней странице',  #callbask answer
    'simulator_first_page': 'Вы уже находитесь на первой странице',  # callbask answer
    'simulator_check_word' : '<code>Перевод верный, но мне нужно другое слово, попробуй ещё раз</code>',
    'simulator_true_end_1' : '<code>Тест завершён,вы выучили следующие слова:\n</code>',
    'simulator_true_end_2': '<code>Для выхода используйте кнопку /main_menu.</code>',
    'simulator_false_end': '<code>Тест завершён, новых слов не было изучено. Для выхода используйте кнопку /main_menu из пункта меню слева внизу экрана.</code>',
    'simulator_new_error' : '️⚠️ На данный момент у вас нет новых слов для изучения.'
}

LEXICON_REMINDER: dict[str, str] = {
    'reminder_absent': '<code>Напоминание отсутствует.</code>',
    'reminder_on' : '<code>Введите на какое время необходимо установить ежедневное напоминание(в формате H:M)</code>',
    'reminder_delete' : 'Напоминание успешно удалено',       #callbask answer
    'reminder_format_time' : 'Время должно быть в формате H:M(часы:минуты)',  #callbask answer
    'reminder_start' : '⚠️ Для того чтобы начать тест вы должны быть в главном меню.',         #callbask answer
    'reminder_send_message' : '<code>Пора пройти тест по новым словам</code>',
}

LEXICON_DICT: dict[str, str] = {
    'dict_empty': '<code>На данный момент словарь пуст.</code>',
    'dict_add' : 'Message added successfully',   #callbask answer
    'dict_add_err': 'Данное слово уже добавлено',  # callbask answer,

}

LEXICON_KEYBOARD: dict[str, str] = {
    'dicts': ' 📚 Словари',
    'simulator' : '🪬 Тренажёры',
    'reminder': '📌 Напоминание',
    'dict_all': '📕 Словарь со всеми словами',
    'dict_new': '📗 Словарь с новыми словами',
    'dict_learned': '📘 Словарь с изученными словами',
    'simulator_all': '🔸 Тренажёр по всем словам',
    'simulator_new' : '🔹 Тренажёр по новым словам',
    'simulator_gpt': '🔻 Тренажёр с GPT',
    'reminder_true_kb' : '❎ Отключить',
    'reminder_false_kb' : '✅ Включить',
    'scheduler_kb' : '➯ Начать',
    'dict_add' : '➕ Добавить в словарь',
    'back': '🔙 Назад',
    'simulator_new_start_kb' : '➯ Начать'
}


LEXICON_MAIN_MENU: dict[str,str] = {
    '/main_menu' : 'Главное меню',
    '/add_word' : 'Добавить слово'

}