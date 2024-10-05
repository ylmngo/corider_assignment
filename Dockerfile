FROM python:3.9-slim 

WORKDIR /app 

COPY . /app 

RUN pip install -r requirements.txt 

ENV FLASK_APP=core/server.py
ENV MONGO_HOST="mongodb"
ENV MONGO_PORT="27017" 

EXPOSE 8000 

CMD ["gunicorn", "--config", "gunicorn_config.py", "core.server:app"]