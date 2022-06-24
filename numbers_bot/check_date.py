import db
import datetime
from dateutil.relativedelta import relativedelta
import sys
import numbers_bot
import asyncio

def check_date_delivery(chat_id: str,
                        last_expired_orders: tuple) -> tuple:
    '''Получение заказов с истекшем сроком поставки и отрправка уведомления об этом'''
    conn = db.connect_db()
    cursor = conn.cursor()

    current_date = datetime.date.today()
    lower_bound = current_date - relativedelta(months=1)

    cursor.execute("SELECT number_order FROM orders "
                   f"WHERE delivery_time >= '{lower_bound}' "
                   f"AND delivery_time < '{current_date}'")

    expired_orders = tuple(row[0] for row in cursor.fetchall())

    #Получаем новые заказы с истекшим сроком поставки с последнего просмотра 
    new_expired_orders = tuple(set(expired_orders).difference(set(last_expired_orders)))

    if new_expired_orders:
        message = ("У заказов "
        f"{', '.join(map(lambda row: '№' + str(row), new_expired_orders))} "
        "прошел срок доставки")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(numbers_bot.send_notify(int(chat_id), message))

    conn.close()
    return expired_orders

def main():
    chat_id = sys.argv[1]
    last_expired_orders = tuple()
    while True:
        last_expired_orders = check_date_delivery(chat_id,
                                                  last_expired_orders)

if __name__=='__main__':
    main()