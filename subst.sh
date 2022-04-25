sed -e "s/__ZIP__/$(base64 -w 0 src.zip | sed 's:/:\\/:g')/" run.sh
