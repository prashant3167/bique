# FROM python:3.9.10
FROM pacific31/formatter_hadoop:latest
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY src/ /app
WORKDIR /app
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
