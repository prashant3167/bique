FROM python:3.9.10
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY src/ /app
WORKDIR /app
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
