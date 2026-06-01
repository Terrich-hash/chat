FROM python:3.12-slim

WORKDIR /app

COPY . .

EXPOSE 12345

CMD ["python", "app/server.py"]