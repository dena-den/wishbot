from aiogram import executor
from app.logic.bot import dp


if __name__ == "__main__":
    print("Starting..")
    executor.start_polling(dp, skip_updates=True)
