FROM python:3.8-slim-buster
RUN pip install katcr==3.0.0
ENTRYPOINT ["katcr"]
