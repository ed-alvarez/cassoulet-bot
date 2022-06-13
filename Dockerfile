FROM python:3.10.2-alpine3.15

WORKDIR /usr/src

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "cassoulet"]
