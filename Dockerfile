FROM python:3.7-slim
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN apt-get update && pip install --upgrade pip && apt-get -y install libpq-dev gcc && pip install psycopg2
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["flask", "run", "--host=0.0.0.0", "--port=80", "--reload"]
