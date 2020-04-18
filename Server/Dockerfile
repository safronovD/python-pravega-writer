FROM python:3.7

ENV ROOT=/usr/src/app

WORKDIR ${ROOT}
ADD . ${ROOT}
RUN pip install -r requirements.txt

CMD ["python", "main.py"]