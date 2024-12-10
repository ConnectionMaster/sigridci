FROM python:3.11-alpine

RUN apk --no-cache -U upgrade && \
    apk --no-cache add git

COPY sigridci /sigridci
RUN git config --global --add safe.directory '*'

ENTRYPOINT ["/sigridci/sigridci.py"]
