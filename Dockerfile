FROM python:3.7-bookworm

WORKDIR /code

COPY . /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python" ]

CMD ["server.py" ]