# Flask REST api.
Source code for the "VideoRecorder" project.
It is a prototype of project that can be a basement for REST service.
There are used such technologies as Flask, SQLAlchemy

## How to start project on your local computer (the most complicated way)
- Requirements
You need python 3.6+, virtual environment or install all packages locally
- [Python](https://www.python.org/downloads/g) 3.6 or later 
- [venv python 3.5](https://docs.python.org/3/library/venv.html)

- 1 Install requirements
```
pip3 install -r requirements.txt
``` 

- 2 Init database
```
export FLASK_APP=lucky_club/lucky_club.py
flask initdb
```

- 3 Run application
```
$ python application.py
```

## Start project in docker container (I think the easiest way to run REST API)
Run that commands
```
docker build -t videorecorder -f Dockerfile  .

docker run -p 5000:5000 --name videorecorder videorecorder
```
