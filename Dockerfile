FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3 python3-pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ssl_api.py /opt/ssl_api.py
COPY inventory.txt inventory.txt

CMD ["python3", "/opt/ssl_api.py"]


