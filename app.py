from utils.db_api.db_gino import create_db


#async def on_startup():
    #await create_db()


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp)
