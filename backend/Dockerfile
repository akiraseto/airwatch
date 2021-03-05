FROM python:3.8

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system

WORKDIR /root/backend
ENV PYTHONPATH /root/backend

CMD ["python", "app.py"]
