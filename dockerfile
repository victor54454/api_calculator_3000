FROM docker.io/python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY test_main.py .
COPY run_test.sh .
COPY main.py .

RUN chmod +x run_test.sh
RUN chmod +x test_main.py

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest httpx


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
