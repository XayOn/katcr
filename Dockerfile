FROM python:3.6.2
RUN pip install katcr
CMD ["katcr_bot", "--token_file", "/volume/token"]
