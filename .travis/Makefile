SUPERCOLLIDER_DIR = ${TRAVIS_BUILD_DIR}/supercollider
SUPERCOLLIDER_BUILD_DIR = $(SUPERCOLLIDER_DIR)/BUILD

get-type-hints:
	pip install --target /tmp/typehints --no-deps uqbar>=0.3.2

install-scsynth:
	cd ${TRAVIS_BUILD_DIR} && \
		git clone -q https://github.com/supercollider/supercollider.git
	cd $(SUPERCOLLIDER_DIR) && \
		git checkout -q ${SUPERCOLLIDER_VERSION} && \
		git submodule -q init && \
		git submodule -q update && \
		mkdir BUILD
	cd $(SUPERCOLLIDER_BUILD_DIR) && \
		cmake \
			-DCMAKE_BUILD_TYPE=Release \
			-DSC_EL=OFF \
			-DSC_IDE=OFF \
			-DSC_QT=OFF \
			-Wno-dev \
			$$TRAVIS_BUILD_DIR/supercollider > /dev/null
	cd $(SUPERCOLLIDER_BUILD_DIR) && make > /dev/null
	cd $(SUPERCOLLIDER_BUILD_DIR) && sudo make install > /dev/null
	scsynth -v  # sanity check
	mkdir -p /home/travis/.local/share/SuperCollider/
	chown -R travis:travis /home/travis/.local/

pytest:
	cd ${TRAVIS_BUILD_DIR} && \
	pytest \
		--durations=100 \
		--timeout=60 \
		tests/test_realtime_Server_boot.py \
		tests/test_synthdefs_SynthDefCompiler_basic.py \
		tests/ \
		supriya/

sanity-check:
	python -c 'import supriya; server = supriya.Server.default().boot(); print(server); server.quit()'

setup-audio:
	sudo usermod -a -G audio travis
