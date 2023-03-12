FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update
RUN pip install -r requirements.txt
COPY . /app
CMD [ "python", "./main.py"]
