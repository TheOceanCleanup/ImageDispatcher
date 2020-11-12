FROM python:3.7-alpine

# Install build dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --virtual=build gcc libffi-dev musl-dev openssl-dev make cmake g++

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

CMD python main.py