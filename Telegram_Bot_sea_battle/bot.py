import asyncio
import logging
from aiogram import Bot,Dispatcher
from handlers import user_handlers,admin_handlers
from config_data.config import Config,load_config
from keyboards.main_menu import set_main_menu
# from handlers.user_handlers import storage

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s'
                               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token,parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    await set_main_menu(bot)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



#Добавлено главное меню при старте
#Добавлен чат в сражении
#Изменена расстановка кораблей
#Изменена анимация при сражении

# Требуют доработки - история побед чтобы сохранялась в БД
# При установке кораблей сделать чтобы лишние сообщения исчезали.

#Проерить когда ожидаешь ответа оппонента и напишешь в чат кому придёт сообщение
