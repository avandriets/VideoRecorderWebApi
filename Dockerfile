FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install psycopg2
 RUN pip install -r requirements.txt
 ADD . /code/
 ENV FLASK_APP=/code/recorder/recorder.py
 RUN flask initdb

 EXPOSE 5000
# one user service
# CMD ["python", "application.py"]
CMD ["gunicorn", "wsgi:application", "-b", "0.0.0.0:5000", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0"]
