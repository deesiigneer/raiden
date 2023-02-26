FROM python:3.9-slim

WORKDIR /raiden
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

ENV WBHOOK_URL=$WBHOOK_URL
ENV BOT_TOKEN=$BOT_TOKEN
ENV SP_CARD_ID=$SP_CARD_ID
ENV SP_TOKEN=$SP_TOKEN

COPY . .

CMD ["python", "main.py"]
