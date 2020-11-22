FROM python:3.8-slim-buster
RUN pip install katcr==3.0.3
ENTRYPOINT ["katcr"]
