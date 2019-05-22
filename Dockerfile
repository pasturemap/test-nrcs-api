FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get -qq install \
        build-essential \
        cython3 \
        python3-dev \
        python3-gdal \
        python3-cartopy \
        python3-pip \
        python3-geopandas \
        libproj-dev \
        libgdal-dev \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install \
    contextily \
    dataclasses \
    geoplot

RUN mkdir -p /opt/project
WORKDIR /opt/project

COPY . ./
