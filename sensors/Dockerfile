FROM python:3.8

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install vim

RUN pip install requests pymongo python-dotenv smbus2 RPi.GPIO

RUN git clone https://github.com/adafruit/Adafruit_Python_BMP.git && \
    cd /Adafruit_Python_BMP && \
    python setup.py install

RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git && \
    cd  /Adafruit_Python_DHT && \
    python setup.py install

WORKDIR /root/sensors
ENV PYTHONPATH /root/sensors

CMD ["python", "app.py"]
