FROM python:3.8.12-alpine3.14


# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt; exit 0
RUN python -c "from pyppeteer.chromium_downloader import download_chromium; download_chromium()"

# copy project
COPY . /usr/src/app/
