FROM resin/rpi-raspbian:jessie-20170111

RUN apt-get update
RUN apt-get install -y  --no-install-recommends \
    python3-pip \
    python3-dev \
    gcc \
    python3-numpy \
    python3-pandas

RUN pip3 install flask pymongo flask-cors

WORKDIR /root/backend
ENV PYTHONPATH /root/backend

CMD ["python3", "app.py"]
