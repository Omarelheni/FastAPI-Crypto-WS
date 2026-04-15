FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
