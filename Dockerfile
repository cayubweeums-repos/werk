# ARG PYTHON_VERSION=3.12.1

FROM ubuntu:22.04

ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y python3 python3-pip git && apt-get clean

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 5554

# Run the application.
CMD python3 main.py