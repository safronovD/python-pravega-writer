FROM python:3.8-slim

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

COPY ../common/log ${ROOT}/log
ADD server/config.yaml ${ROOT}
ADD server/main.py ${ROOT}
ADD server/requirements.txt ${ROOT}

RUN pip --no-cache-dir install -r requirements.txt
RUN mkdir data

EXPOSE 666

ENTRYPOINT ["python", "main.py"]