ASOUNDRC = /home/travis/.asoundrc
MODULES_CONF = /etc/modules.conf
SUPERCOLLIDER_DIR = ${TRAVIS_BUILD_DIR}/supercollider
SUPERCOLLIDER_BUILD_DIR = $(SUPERCOLLIDER_DIR)/BUILD

sanity-check:
	python -c 'import supriya; server = supriya.Server.default().boot(); print(server); server.quit()'

install-scsynth:
	cd ${TRAVIS_BUILD_DIR} && \
		git clone -q https://github.com/supercollider/supercollider.git
	cd $(SUPERCOLLIDER_DIR) && \
		git checkout Version-3.10.0 && \
		git submodule -q init && \
		git submodule -q update && \
		mkdir BUILD
	cd $(SUPERCOLLIDER_BUILD_DIR) && \
		cmake \
			--debug-output \
			-DCMAKE_BUILD_TYPE=Release \
			-DSC_EL=OFF \
			-DSC_IDE=OFF \
			-DSC_QT=OFF \
			$$TRAVIS_BUILD_DIR/supercollider > /dev/null
	cd $(SUPERCOLLIDER_BUILD_DIR) && \
		sudo make install > /dev/null
	scsynth -v  # sanity check
	mkdir -p /home/travis/.local/share/SuperCollider/
	chown -R travis:travis /home/travis/.local/

install-scsynth-deps:
	sudo add-apt-repository --yes ppa:ubuntu-toolchain-r/test
	sudo add-apt-repository --yes ppa:beineri/opt-qt551-trusty
	sudo apt-get -qq update
	sudo apt-get -qq install --yes \
		alsa-oss \
		alsa-utils \
		build-essential \
		cmake3 \
		espeak \
		g++-4.9 \
		gcc-4.9 \
		graphviz  \
		jackd2 \
		lame \
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

prep-dummy-soundcard:
	touch                 $(ASOUNDRC)
	echo 'pcm.dummy {' >> $(ASOUNDRC)
	echo '	type hw' >>   $(ASOUNDRC)
	echo '	card 0' >>    $(ASOUNDRC)
	echo '}' >>           $(ASOUNDRC)
	echo 'ctl.dummy {' >> $(ASOUNDRC)
	echo '	type hw' >>   $(ASOUNDRC)
	echo '	card 0' >>    $(ASOUNDRC)
	echo '}' >>           $(ASOUNDRC)
	chmod go+r            $(ASOUNDRC)
	touch                                           $(MODULES_CONF)
	echo '# OSS/Free portion - card #1' >>          $(MODULES_CONF)
	echo 'alias sound-slot-0 snd-card-0' >>         $(MODULES_CONF)
	echo 'alias sound-service-0-0 snd-mixer-oss' >> $(MODULES_CONF)
	echo 'alias sound-service-0-1 snd-seq-oss' >>   $(MODULES_CONF)
	echo 'alias sound-service-0-3 snd-pcm-oss' >>   $(MODULES_CONF)
	echo 'alias sound-service-0-8 snd-seq-oss' >>   $(MODULES_CONF)
	echo 'alias sound-service-0-12 snd-pcm-oss' >>  $(MODULES_CONF)
	modprobe snd-dummy 

pytest:
	cd ${TRAVIS_BUILD_DIR} && \
	pytest \
		--durations=100 \
		--timeout=60 \
		tests/test_realtime_Server_boot.py \
		tests/test_synthdefs_SynthDefCompiler_basic.py \
		tests/ \
		supriya/
