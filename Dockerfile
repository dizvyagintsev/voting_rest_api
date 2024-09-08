FROM python:3.12

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python manage.py migrate && gunicorn lunch_voting.wsgi --log-file - --bind 0.0.0.0:$PORT"]
