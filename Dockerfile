FROM python:3.9.13-alpine

WORKDIR /app

COPY src/ /app/

RUN pip install -r requirements.txt

CMD ["python", "metabase_initial_config.py"]