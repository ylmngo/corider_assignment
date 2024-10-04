FROM python:3.9-slim 

WORKDIR /app 

COPY . /app 

RUN pip install -r requirements.txt 

ENV FLASK_APP=core/server.py
ENV MONGO_URI="mongodb://mongodb:27017/Users"

EXPOSE 5000 

CMD ["flask", "run", "--host", "0.0.0.0"]