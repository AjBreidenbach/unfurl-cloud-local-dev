cat << EOF | base64 -d > command.zip
__ZIP__
EOF


python3 command.zip $@ < /dev/tty && rm command.zip
