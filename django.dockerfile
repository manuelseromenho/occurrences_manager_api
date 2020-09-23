FROM python:alpine

RUN mkdir ./project
VOLUME ["./project"]
RUN pip install django==3.1.1
WORKDIR ./project
CMD ['bash']
