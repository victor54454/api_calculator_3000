FROM docker.io/python:3.13-slim

# SÉCURITÉ: Créer un utilisateur non-root
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --create-home appuser

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
USER appuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
