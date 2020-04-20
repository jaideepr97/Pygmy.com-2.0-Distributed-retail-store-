FROM python:3.6.1-alpine
ENV LOG_FILE_NAME front_end_server_log.txt
WORKDIR /src
ADD . /src
RUN pip3 install -r requirements.txt
CMD python3 front-end.py $LOG_FILE_NAME