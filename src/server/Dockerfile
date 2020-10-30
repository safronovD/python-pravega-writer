FROM python:3.8-slim

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

COPY common/log ${ROOT}/log
COPY server/core ${ROOT}/core
ADD server/config.yaml ${ROOT}
ADD server/main.py ${ROOT}
ADD server/requirements.txt ${ROOT}

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 666

ENTRYPOINT ["python", "main.py"]