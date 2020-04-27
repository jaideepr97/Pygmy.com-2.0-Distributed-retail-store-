FROM python:3.6.1-alpine
ENV PORT 34612
ENV DB_CONN_STRING sqlite:///catalog_B.db
ENV REPLICA_PORT 34602
ENV LOG_FILE_NAME catalog_B_log.txt
ENV OUTPUT_FILE_NAME catalog_B_output.txt
WORKDIR /src
ADD . /src
RUN pip3 install -r requirements.txt
CMD python3 catalogue.py $PORT $DB_CONN_STRING $REPLICA_PORT $LOG_FILE_NAME $OUTPUT_FILE_NAME