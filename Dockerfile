FROM python:3-alpine
COPY *.html /www/
COPY en /www/en
COPY assets /www/assets
WORKDIR /www
CMD ["python3", "-m", "http.server", "8080"]
