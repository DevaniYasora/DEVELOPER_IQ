FROM python:3.11-slim-bullseye

WORKDIR /app
COPY ./requirements.txt /app/

RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5006

CMD ["python", "productivity_calculation.py"]

