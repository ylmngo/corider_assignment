FROM python:3.9-slim 

WORKDIR /app 

COPY . /app 

RUN pip install -r requirements.txt 

ENV FLASK_APP=core/server.py
ENV MONGO_URI="mongodb://mongodb:27017/Users"

EXPOSE 8000 

CMD ["gunicorn", "--config", "gunicorn_config.py", "core.server:app"]