FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY first_django_project .

CMD ["gunicorn", "first_django_project.wsgi:application", "--bind", "0.0.0.0:8000"]

