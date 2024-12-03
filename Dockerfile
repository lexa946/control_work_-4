FROM python:3.12-slim

LABEL authors="APozhar"


COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]


