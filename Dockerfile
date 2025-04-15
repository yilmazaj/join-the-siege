FROM python:3.12.10-slim

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y curl libgl1 tesseract-ocr && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD ["python", "-m", "app"]


