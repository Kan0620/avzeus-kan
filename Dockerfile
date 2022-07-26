FROM python:3.8.13

COPY ./requirements.txt /requirements.txt

RUN pip install -U pip \
    && pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
