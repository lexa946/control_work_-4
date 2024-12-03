import json

from app.dao import ProductDAO


async def add_mock_data():
    with open("data_mock.json", encoding="UTF-8") as json_file:
        mock_data = json.load(json_file)
    for data in mock_data:
        await ProductDAO.insert_data(**data)
