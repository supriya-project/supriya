#!/bin/bash

git clone -q https://github.com/supercollider/supercollider.git
cd $TRAVIS_BUILD_DIR/supercollider && \
    git checkout Version-3.10.0 && \
    git submodule -q init && \
    git submodule -q update && \
    mkdir BUILD

cd $TRAVIS_BUILD_DIR/supercollider/BUILD && \
cmake \
    --debug-output \
    -DCMAKE_BUILD_TYPE=Release \
    -DSC_EL=OFF \
    -DSC_IDE=OFF \
    -DSC_QT=OFF \
    $TRAVIS_BUILD_DIR/supercollider > /dev/null

cd $TRAVIS_BUILD_DIR/supercollider/BUILD && \
sudo make install > /dev/null

scsynth -v  # sanity check
