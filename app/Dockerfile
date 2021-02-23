FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["sh", "entrypoint.sh"]