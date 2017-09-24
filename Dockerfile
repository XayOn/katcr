FROM python:3.6.2
RUN pip install katcr
ARG token
CMD ["/bin/bash", "-c", "katcr_bot --token `cat /volume/token`"]
