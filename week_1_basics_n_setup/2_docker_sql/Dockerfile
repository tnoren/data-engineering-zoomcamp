FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY notebook.py notebook.py

ENTRYPOINT [ "python", "notebook.py" ]