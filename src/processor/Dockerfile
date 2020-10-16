FROM python:3.8-slim

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

COPY common/log ${ROOT}/log
ADD processor/config.yaml ${ROOT}
ADD processor/main.py ${ROOT}
ADD processor/requirements.txt ${ROOT}

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 666

ENTRYPOINT ["python", "main.py"]