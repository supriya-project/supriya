FROM python:3.5.2

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /supriya

RUN apt-get update && apt-get -y install software-properties-common && \
    #add-apt-repository --yes ppa:ubuntu-toolchain-r/test && \
    #add-apt-repository --yes ppa:beineri/opt-qt551-trusty && \
    apt-get update && \
    apt-get install --yes \
        build-essential \
        gcc-4.9 \
        g++-4.9 \
        cmake \
        pkg-config \
        libjack-jackd2-dev \
        libsndfile1-dev \
        libasound2-dev \
        libavahi-client-dev \
        libreadline6-dev \
        libfftw3-dev \
        libicu-dev \
        libxt-dev \
        libudev-dev && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.9 && \
    update-alternatives --auto gcc

RUN git clone https://github.com/supercollider/supercollider.git /supercollider && \
    cd /supercollider && \
    git submodule init && git submodule update && \
    cmake -DSC_EL=OFF -DSC_QT=OFF -DSC_IDE=OFF \
        -DCMAKE_INSTALL_PREFIX:PATH=/usr/local \
        -DCMAKE_BUILD_TYPE=Release /supercollider --debug-output && \
    make install

COPY . /supriya

RUN pip install -U pip && \
    pip install -e .

CMD ["bash"]
