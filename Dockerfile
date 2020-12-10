FROM debian:buster-slim
LABEL maintainer="Noah Sandman <noah@modulytic.com>"

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -qq gammu gammu-smsd python3-pip git

RUN mkdir /app
WORKDIR /app

# create blank expected files, these can be replaced with volumes if needed
RUN touch ./smsdrc-user
RUN touch ./on_receive
RUN chmod +x ./on_receive
RUN touch ./requirements.txt
RUN mkdir ./smsdrcs

# copy and run configuration script
COPY script/config.py ./config.py

# Start all daemons
COPY script/run.sh ./run.sh
RUN chmod +x ./run.sh
ENTRYPOINT ["./run.sh"]
