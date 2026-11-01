FROM python:3-alpine
COPY *.html /www/
COPY assets /www/assets
WORKDIR /www
CMD ["python3", "-m", "http.server", "8080"]
