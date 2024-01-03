FROM python:3.11

WORKDIR /pythonProject9

COPY . /pythonProject9

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV NAME World

CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]
