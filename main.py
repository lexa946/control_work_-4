import asyncio

from app.dao import ProductDAO
from app.database import drop_tables, create_tables
from app.helpers import add_mock_data


async def main():
    await drop_tables()
    await create_tables()
    await add_mock_data()

    print("Общая выручка:", await ProductDAO.get_total_revenue())
    print("Товары по категориям:", dict(await ProductDAO.get_items_by_category()))

    min_price = 1.0
    print(f"Покупки дороже {min_price}:",await ProductDAO.get_expensive_purchases(min_price))

    print("Средняя цена по категориям:", await ProductDAO.get_average_price_by_category())
    print("Категория с наибольшим количеством проданных товаров:", await ProductDAO.get_most_frequent_category())


if __name__ == '__main__':
    asyncio.run(main())