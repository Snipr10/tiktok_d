#FROM python:3.8.12-alpine3.14

FROM buildkite/puppeteer:10.0.0

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev -y

RUN wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz && tar -xvzf Python-3.9.6.tgz && cd Python-3.9.6 && \
    ./configure --enable-optimizations && make altinstall && \
    update-alternatives --install /usr/bin/python python /usr/local/bin/python3.9 1 && \
    python -m ensurepip --upgrade && wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

RUN apt install -y gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget libcairo-gobject2 libxinerama1 libgtk2.0-0 libpangoft2-1.0-0 libthai0 libpixman-1-0 libxcb-render0 libharfbuzz0b libdatrie1 libgraphite2-3 libgbm1


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
