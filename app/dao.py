from collections import defaultdict

from sqlalchemy import select, text
from sqlalchemy.sql.functions import sum, count
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.models import Product


class ProductDAO:

    @classmethod
    async def insert_data(cls, **data):
        async with async_session_maker() as session:
            item = Product(**data)
            session.add(item)
            await session.commit()
            return item

    @classmethod
    async def get_total_revenue(cls) -> float | int:
        async with async_session_maker() as session:
            session: AsyncSession

            query = select(
                sum(Product.price * Product.quantity)
            )
            return await session.scalar(query)

    @classmethod
    async def get_items_by_category(cls) -> dict:
        categories = defaultdict(list)

        async with async_session_maker() as session:
            session: AsyncSession
            query = select(Product)
            items = await session.scalars(query)

        for item in items:
            categories[item.category].append(item.item)

        return categories

    @classmethod
    async def get_expensive_purchases(cls, min_price: int | float) -> list[dict]:
        async with async_session_maker() as session:
            session: AsyncSession

            query = select(Product).where(Product.price > min_price)
            items = await session.scalars(query)
            return [
                item.as_dict() for item in items.all()
            ]

    @classmethod
    async def get_average_price_by_category(cls) -> dict[str:float | int]:
        async with async_session_maker() as session:
            session: AsyncSession
            # SELECT p.category, avg(price) FROM products p GROUP BY p.category
            items = await session.execute(
                select(
                    Product.category,
                    (sum(Product.price) / count(Product.id))
                ).group_by(Product.category)
            )
            return {key: value for key, value in items.all()}

    @classmethod
    async def get_most_frequent_category(cls) -> str:
        async with async_session_maker() as session:
            session: AsyncSession
            # SELECT p.category FROM products p GROUP BY p.category ORDER BY sum(p.quantity) DESC LIMIT 1
            most_quantity_category = await session.scalar(
                select(Product.category).group_by(Product.category).order_by(sum(Product.quantity).desc()).limit(1))
            return most_quantity_category
