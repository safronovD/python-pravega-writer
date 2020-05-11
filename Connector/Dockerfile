FROM python:3.8-alpine

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

COPY core ${ROOT}/core
COPY config ${ROOT}/config
ADD main.py ${ROOT}
ADD requirements.txt ${ROOT}

RUN pip install -r requirements.txt
RUN mkdir data

ENTRYPOINT ["python", "main.py"]