openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -subj "/C=CN/ST=Beijing/L=Beijing/O=Me/OU=Me/CN=me.org" -keyout key.pem -out cert.pem