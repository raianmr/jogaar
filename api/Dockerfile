FROM python:3.10

WORKDIR /usr/src/api

COPY requirements.txt ./

RUN pip install --no-cache-dir -U -r requirements.txt

COPY . .

CMD uvicorn app.main:app --host 0.0.0.0 --port $API_PORT --reload
