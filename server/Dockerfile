FROM python:3.8-slim

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

ADD config.yaml ${ROOT}
ADD main.py ${ROOT}
ADD requirements.txt ${ROOT}

RUN pip --no-cache-dir install -r requirements.txt
RUN mkdir data

EXPOSE 666

ENTRYPOINT ["python", "main.py"]