FROM python:3.8

ENV PYTHONUNBUFFERED 1

# Install Python and Package Libraries
RUN apt-get update && apt-get install -y libpq-dev gcc postgresql-client \
    python3-dev musl-dev

# Project Files and Settings
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "productimporter.wsgi:application"]