FROM python:3.12-slim

WORKDIR /app

COPY fonts /app/fonts
COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=5000
ENV FLASK_ENV=production

EXPOSE 5000

CMD [ "python", "app.py" ]