FROM python:3.8
COPY . /storelift 
WORKDIR /storelift/api
RUN pip install flask
RUN pip install sqlalchemy
RUN pip install pymysql
RUN export FLASK_APP=app.py
RUN export FLASK_ENV=development
ENTRYPOINT ["python"]
CMD ["app.py"]