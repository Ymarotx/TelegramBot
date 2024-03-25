database: dict[str,dict[str,str]] = {} #БД временная для каждого пользователя со словарём где ключ это имя кто добавил,название тп,геопозиция
database_page: dict[str,dict[str, list[dict[str, str]]]] = {} # Бд временная для сохранения страниц для каждого пользователя
database_quantity_page: dict[str,dict[str,int]] = {} #БД временная для каждого пользователя кол-во страниц.