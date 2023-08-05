FROM ubuntu:18.04

LABEL name="httpbin"
LABEL version="0.9.2"
LABEL description="A simple HTTP service."
LABEL org.httpbin.author="Kenneth Reitz"
LABEL org.httpbin.beginner="Xizhen Du"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ADD requirements.txt .
RUN apt update -y && apt install python3-pip git -y && pip3 install --no-cache-dir pipenv && pip3 install --no-cache-dir -r requirements.txt


ADD Pipfile Pipfile.lock /httpbin/
WORKDIR /httpbin
RUN /bin/bash -c "pip3 install --no-cache-dir -r <(pipenv lock -r)"

ADD . /httpbin
RUN pip3 install --no-cache-dir /httpbin

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "httpbin:app", "-k", "gevent"]
