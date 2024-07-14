FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY service / app/
WORKDIR /app
EXPOSE 8000


RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt