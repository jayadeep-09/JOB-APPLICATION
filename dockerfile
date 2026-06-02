FROM python:3.14

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn", "job.wsgi:application", "--bind", "0.0.0.0:10000"]
