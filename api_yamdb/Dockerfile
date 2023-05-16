FROM python:3.7-slim
WORKDIR /app/
COPY ./ /
RUN find -name 'manage.py'
RUN find -name 'requirements.txt'
RUN find 
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
