#!/bin/bash 

sudo add-apt-repository --yes ppa:ubuntu-toolchain-r/test

sudo add-apt-repository --yes ppa:beineri/opt-qt551-trusty

sudo apt-get -qq update

sudo apt-get -qq install --yes \
    alsa-oss \
    alsa-utils \
    build-essential \
    espeak \
    g++-4.9 \
    gcc-4.9 \
    graphviz  \
    jackd2 \
    libasound2-dev \
    libavahi-client-dev \
    libfftw3-dev \
    libicu-dev \
    libjack-jackd2-dev \
    libreadline6-dev \
    libsndfile1-dev \
    libudev-dev \
    libxt-dev \
    pkg-config

sudo update-alternatives \
    --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 60 \
    --slave /usr/bin/g++ g++ /usr/bin/g++-4.9

sudo update-alternatives --auto gcc
