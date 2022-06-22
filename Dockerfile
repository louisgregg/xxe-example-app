FROM debian:latest
RUN apt -y update && apt -y install python3 python3-pip

ENV FLASK_APP='app'
ENV FLASK_ENV='development'

COPY app /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["flask", "run"]
EXPOSE 5000

