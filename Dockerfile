FROM python:3.12-slim

ARG device /dev/video0

WORKDIR /app

ADD main.py .
ADD config.py .
ADD draw.py .
ADD telegram.py .

RUN pip install opencv-contrib-python-headless
RUN pip install requests

CMD ["python", "./main.py"]
