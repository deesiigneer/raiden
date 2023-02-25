FROM python:3.9-slim

WORKDIR /raiden
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
