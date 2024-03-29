FROM python:3.7-alpine

# Install build dependencies
RUN apk update && apk add gcc python3-dev musl-dev
RUN apk add --virtual=build gcc libffi-dev musl-dev openssl-dev make cmake g++

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ARG GIT_BRANCH=unspecified
LABEL git_branch=$GIT_BRANCH
ENV GIT_BRANCH=$GIT_BRANCH

ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

ARG VERSION=unspecified
LABEL version=$VERSION
ENV VERSION=$VERSION

CMD python main.py