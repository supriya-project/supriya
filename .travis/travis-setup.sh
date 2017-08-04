#! /usr/bin/env bash
cat > ~/.jackdrc <<EOF
/usr/bin/jackd -ddummy -r48000 -p1024
EOF
sudo su -c 'echo load-module module-jack-source channels=2 connect=false >> /etc/pulse/default.pa'
sudo su -c 'echo load-module module-loopback source=jack_in >> /etc/pulse/default.pa'
sudo su -c 'echo @audio - rtprio 99 >> /etc/security/limits.d/audio.conf'
sudo su -c 'echo @audio - memlock unlimited >> /etc/security/limits.d/audio.conf'
sudo su -c 'echo @audio - nice -10 >> /etc/security/limits.d/audio.conf'
sudo su -c 'echo realtime-scheduling = yes >> /etc/pulse/daemon.conf'