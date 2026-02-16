FROM python:3.9

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY sentinel.py .

RUN mkdir -p logs

CMD ["python", "-u", "sentinel.py"]