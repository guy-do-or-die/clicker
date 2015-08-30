#! /bin/bash

if [ ! -f ~/bin/chtomedriver ]; then
	wget 'http://chromedriver.storage.googleapis.com/2.18/chromedriver_linux64.zip'
	unzip -o *.zip -d ~/bin
	chown $USER ~/usr/bin/chromedriver
	rm *.zip
fi;

virtualenv .env
. .env/bin/activate

apt-get install tor
apt-get install privoxy

cp /etc/privoxy/config /etc/privoxy/config.bak
echo 'echo "forward-socks5 / localhost:9050 ." >> /etc/privoxy/config' | sudo -s 
