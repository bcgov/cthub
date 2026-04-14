FROM python:3.14.4

ENV PYTHONUNBUFFERED=1

WORKDIR /api
COPY . /api/
RUN pip install -r requirements.txt

# Place to store static files
RUN mkdir /frontend
RUN mkdir /frontend/public
