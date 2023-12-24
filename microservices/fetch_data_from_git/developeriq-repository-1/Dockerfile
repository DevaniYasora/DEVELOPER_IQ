FROM python:3.11-slim-bullseye

WORKDIR /app
COPY ./requirements.txt /app/

RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5004

CMD ["python", "fetch_data_from_git.py"]

