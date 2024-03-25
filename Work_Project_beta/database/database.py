application: dict[str,str] = {}

application_page: dict[str, list[dict[str, str]]] = {}
application_page_stock: dict[str,list] = {}

database: dict[str,int] = {} # Первый ключ quantity_page(кол-во страниц  для application)
                             # Второй ключ user_page(на какой странице юзер)
                             # Третий ключ db_id - id строчки из таблицы при active_application,cancel_application
                            # Четвёртый ключ quantity_page_close(кол-во страниц  для close_application)
                            #Пятый ключ quantity_page_cancel кол-во страниц для cancel_application
                            #Шестой ключ quantity_page_stock кол-во страница для stock
                            #Седьмой ключ purchase_page кол-во страниц для purchase
                            #Восьмой ключ id_notes id примечания
                            #Девятый ключ notes_del айди сообщения на удаление
                            #Десятый ключ count_incorr_answer кол-во неправильных ответов которые можно дать до появления подсказки

database_str: dict[str,str] = {} #Первый ключ callback сохранённый callback_data в stock_press,
                                # Второй ключ time_schedule хранит строку со временем для планировщика


database_2: dict[str,str] = {} #БД для отметки после нажатия при выборе материалов.
                                #cable_kb,internal_sockets_kb,external_sockets_kb и т.д.,
#                               Использую как ключ closing_app для хранения названия материала после ввода кол-ва.
database_3: list = [] #БД для очистки лексикона,храним те лексиконы которые будем очищать.
database_4: dict = {} #Храним callback с названием месяца для детальной информации в итогах за месяц по ключу month
database_5: dict = {} #Используем для меню Склад в stock.py и при добавлении записи или удалении в user_handlers
database_6: dict = {} #Используем при stock_press_press

database_time: dict[str,str] = {} #ключ time для закрытия заявки записывает время для всех чтобы было одинаковое для одной заявки

db_name_materials: list[str] = [] #Храним: [0] - имя таблицы,[1] - имя стобца,[2] - число для записи в табллицу

database_materials: dict[str,dict] = {} #Храним данные из db_name_material как временное хранилище и потом
                                    #добавляь только в БД постоянную.

db_material_table: dict[str,dict[str,dict[str,str]]] = {} #Словарь содержит название таблицы
                                                    #со словарём название столбца со словарём дата и кол-во.

database_del: list = [] #БД для удаления сообщений
database_english_list: list = []
database_english_dict: dict[str,str] = {}
database_english_answer: list = [] #СОдержит один ответ на один вопрос.
database_closing_app: dict[str,int] = {}