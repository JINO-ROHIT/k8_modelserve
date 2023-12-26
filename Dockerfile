FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 80

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "80"]
