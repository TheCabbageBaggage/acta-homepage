FROM python:3-alpine
COPY index.html /www/index.html
WORKDIR /www
CMD ["python3", "-m", "http.server", "8080"]
