FROM python:3.11
RUN apt-get update && apt-get install -y git
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
RUN git clone https://region74:${GITHUB_TOKEN}@github.com/region74/CheloncoBot.git /app \
    && cd /app \
    && git checkout master \
    && git pull
WORKDIR /app
COPY .env /app/.env
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
CMD ["sh", "-c", "make migrate && python -u main.py"]