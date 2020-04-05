FROM python:3.7

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}

ADD requirements.txt ${ROOT}/requirements.txt

RUN pip install -r requirements.txt

ADD . ${ROOT}

CMD ["python", "main.py"]