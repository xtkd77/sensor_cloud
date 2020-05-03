# our base image
FROM ubuntu

# Install python and pip
RUN apt update -y
RUN apt install python3  -y -qq --no-install-recommends 
RUN apt install python3-pip -y -qq  --no-install-recommends
RUN apt install python3-setuptools -y -qq  --no-install-recommends
RUN pip3 install --upgrade pip

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY main.py /usr/src/app/
COPY mqttkey  /usr/src/app/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python3", "/usr/src/app/main.py"]