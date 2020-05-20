FROM python:3.8-alpine

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

ADD main.py ${ROOT}
ADD requirements.txt ${ROOT}

RUN apk --no-cache add musl-dev linux-headers g++
RUN pip install -r requirements.txt
RUN mkdir data

ENTRYPOINT ["python", "main.py"]