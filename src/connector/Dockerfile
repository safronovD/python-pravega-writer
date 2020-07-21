FROM python:3.8-slim

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

COPY common/log ${ROOT}/log
COPY connector/core ${ROOT}/core
ADD connector/config.yaml ${ROOT}
ADD connector/main.py ${ROOT}
ADD connector/requirements.txt ${ROOT}

RUN pip --no-cache-dir install -r requirements.txt
RUN mkdir data

ENTRYPOINT ["python", "main.py"]