FROM python:3.8-slim

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

COPY core ${ROOT}/core
ADD config.yaml ${ROOT}
ADD main.py ${ROOT}
ADD requirements.txt ${ROOT}

RUN pip --no-cache-dir install -r requirements.txt
RUN mkdir data

ENTRYPOINT ["python", "main.py"]