FROM python:3.8-slim

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

COPY common/log ${ROOT}/log
COPY ml-controller/core ${ROOT}/core
ADD ml-controller/config.yaml ${ROOT}
ADD ml-controller/main.py ${ROOT}
ADD ml-controller/requirements.txt ${ROOT}

RUN pip --no-cache-dir install -r requirements.txt
RUN mkdir data

ENTRYPOINT ["python", "main.py"]