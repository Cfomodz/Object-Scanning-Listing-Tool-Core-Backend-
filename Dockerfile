FROM python:3.13.2-alpine3.21@sha256:323a717dc4a010fee21e3f1aac738ee10bb485de4e7593ce242b36ee48d6b352
ENV FLASK_APP=app.py \
    FLASK_ENV=production
RUN apk add --no-cache \
    libjpeg-turbo-dev \
    zlib-dev \
    zbar-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/logs /app/data
EXPOSE 5000
CMD ["python", "app.py"] 