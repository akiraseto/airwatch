FROM python:3.8

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system

WORKDIR /root/sensors
ENV PYTHONPATH /root/sensors

CMD ["python", "app.py"]
