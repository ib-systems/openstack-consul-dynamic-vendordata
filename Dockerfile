FROM python:3.12-alpine3.19
WORKDIR /home/ocdv
COPY . .

RUN apk update && apk add gcc libc-dev libffi-dev linux-headers --no-cache && pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "main.py"]