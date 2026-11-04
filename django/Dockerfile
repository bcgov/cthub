FROM python:3.15.2

ENV PYTHONUNBUFFERED=1

WORKDIR /api
COPY . /api/
RUN pip install -r requirements.txt

# Place to store static files
RUN mkdir /frontend
RUN mkdir /frontend/public
