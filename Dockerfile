FROM python:3.11-slim-bookworm

WORKDIR /bot
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m"]

CMD [ "src" ]
