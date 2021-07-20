FROM python:3.9-slim

RUN pip install google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib

COPY token.pickle /home/
COPY credentials.json /home/
COPY delete_cubs_away_games.py /home/

WORKDIR /home

CMD python delete_cubs_away_games.py