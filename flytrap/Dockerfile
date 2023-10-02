FROM python:3.8-alpine


WORKDIR /app


COPY . /app

RUN pip install -r requirements.txt


EXPOSE 80


ENV PYTHONUNBUFFERED=1


CMD ["python", "-u", "flytrap.py"]
