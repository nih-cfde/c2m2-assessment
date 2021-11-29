FROM python:3.9

ADD . /tmp/c2m2-assessment
RUN pip install /tmp/c2m2-assessment
RUN rm -r /tmp/c2m2-assessment

ENTRYPOINT ["c2m2-assessment"]