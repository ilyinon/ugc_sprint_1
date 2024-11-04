FROM python:3.12.4-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/opt/app'

WORKDIR /opt/app
COPY app/requirements.txt /requirements.txt
RUN apt-get update && apt-get install -y git curl netcat-traditional
RUN  pip install --upgrade pip\
     && pip install --no-cache-dir -r /requirements.txt

COPY app/ /opt/app

CMD ["bash", "run_etl.sh"]
