from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from apscheduler.triggers.cron import CronTrigger
from config import Admins, bot
from db import main_db


async def send_notification():
    for admin in Admins:
        products = await main_db.sql_get_products()
        if products:
            for product in products:
                await bot.send_photo(chat_id=admin,
                                     photo=product[5],
                                     caption=f'Name: {product[1]}\n'
                                             f'Size: {product[2]}\n'
                                             f'Category: {product[-2]}\n'
                                             f'Price: {product[3]}\n'
                                             f'Product ID: {product[4]}\n'
                                             f'Product Info: {product[-1]}\n')
        else:
            await bot.send_message(text='There is no products!')


async def set_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_notification,
                      CronTrigger(timezone='Asia/Bishkek',
                                  hour='9',
                                  minute='00',
                                  start_date=datetime.datetime.now()
                                  ),
                      )
    scheduler.add_job(send_notification,
                      CronTrigger(timezone='Asia/Bishkek',
                                  hour='19',
                                  minute='00',
                                  start_date=datetime.datetime.now()
                                  ),
                      )
    scheduler.start()
