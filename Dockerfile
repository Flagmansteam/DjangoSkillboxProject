FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# COPY requirements.txt requirements.txt


RUN pip install --upgrade pip "poetry==1.6.1"
# RUN pip install -r requirements.txt
RUN poetry config virtualenvs.create false --local # poetry не создаёт нового виртуального окружения
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY first_django_project .

CMD ["gunicorn", "first_django_project.wsgi:application", "--bind", "0.0.0.0:8000"]

