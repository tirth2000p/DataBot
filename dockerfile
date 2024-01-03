FROM python:3.11

WORKDIR ./

COPY ./ ./

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]