# our base image
FROM ubuntu:18.04
# see https://hub.docker.com/_/ubuntu/

# Locales
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# For build tools
RUN apt update -y \
   && apt install gcc -y \
   && apt install make -y \
   && apt install vim -y \
   && apt-get install -y less \
   && apt install -y htop

# Install python and pip
RUN apt install python3  -y -qq --no-install-recommends 
RUN apt install python3-pip -y -qq  --no-install-recommends
RUN apt install python3-setuptools -y -qq  --no-install-recommends
RUN pip3 install --upgrade pip

RUN pip3 install --upgrade pip \
  && pip3 install upgrade pip setuptools \
  && pip3 install backtrace \
  && pip3 install paho-mqtt \
  && pip3 install google-cloud-storage \
  && pip3 install google-cloud-pubsub

# Set local directory root
WORKDIR server/gcp

# install Python modules needed by the Python app
#COPY requirements.txt /tmp/
#RUN pip install --no-cache-dir -r /tmp/requirements.txt
#RUN rm /tmp/requirements.txt

# copy files required for the app to run
COPY main.py /usr/src/app/
COPY mqttkey  /usr/src/app/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python3", "/usr/src/app/main.py"]