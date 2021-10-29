FROM python:3.10

RUN pip install --upgrade pip
RUN apt update && apt install supervisor -y

ADD etc etc
WORKDIR /app
ADD . .

RUN pip install . --upgrade
CMD ["/usr/bin/supervisord", "--configuration=/etc/supervisor/supervisord.conf"]
