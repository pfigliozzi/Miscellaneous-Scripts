FROM python:3.9-slim

RUN pip install google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib

COPY token.pickle ~/
COPY credentials.json ~/