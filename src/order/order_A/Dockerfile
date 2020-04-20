FROM python:3.6.1-alpine
ENV PORT 34601
ENV DB_CONN_STRING sqlite:///orders_A.db
ENV LOG_FILE_NAME order_A_log.txt
WORKDIR /src
ADD . /src
RUN pip3 install -r requirements.txt
CMD python3 order.py $PORT $DB_CONN_STRING $LOG_FILE_NAME