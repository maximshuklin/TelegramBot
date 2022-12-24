FROM python:3.10.9-alpine3.17 

WORKDIR ~/TelegramBot

COPY . .

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

CMD ["python3", "bot/test.py"]
