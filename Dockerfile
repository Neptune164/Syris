# syntax=docker/dockerfile:1
FROM python:3.10.1
WORKDIR /Syris
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD [ "python","flask/app.py" ]