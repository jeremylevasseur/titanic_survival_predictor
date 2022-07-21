FROM python:3.9.7
WORKDIR /code
RUN apt-get update -y && apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev -y
ADD ./requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt
ADD . /code
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1

# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["waitress-serve", "--port=5000", "--call", "app:create_app"]
# flask run --host=0.0.0.0
# CMD ["tail", "-F", "/dev/null"] 