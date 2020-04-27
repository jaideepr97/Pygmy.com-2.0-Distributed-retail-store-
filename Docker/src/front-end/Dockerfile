FROM alpine:3.10
RUN apk add --no-cache python3
RUN apk add --update docker openrc
RUN rc-update add docker boot
ENV LOG_FILE_NAME front_end_server_log.txt
ENV OUTPUT_FILE_NAME front_end_server_output.txt
WORKDIR /src
ADD . /src
RUN pip3 install -r requirements.txt
CMD python3 front-end.py $LOG_FILE_NAME $OUTPUT_FILE_NAME