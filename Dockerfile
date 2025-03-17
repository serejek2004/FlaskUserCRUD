FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
