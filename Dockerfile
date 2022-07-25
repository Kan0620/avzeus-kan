FROM python:3.8.13

COPY ./requirements.txt /requirements.txt

RUN pip install -U pip \
    && pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

COPY ./app /app

CMD ["./start.sh"]
