FROM python:3.11.4-slim-buster
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY entrypoint.sh ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

EXPOSE 8010

RUN chmod a+x entrypoint.sh
ENTRYPOINT ["bash", "entrypoint.sh"]