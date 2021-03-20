FROM python:3.7-alpine


ENV FLASK_APP app.py
ENV FLASK_ENV production

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]