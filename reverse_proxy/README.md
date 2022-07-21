# Reverse Proxy Container

The files in this folder are for the reverse proxy.

Within the *nginx.conf* file there are many comments that outline what you need to do if you want to set up an SSL connection. If things are left the way they are, the connection will be through HTTP instead of HTTPS and the browser will indicate to users that the connection is not secure. Follow the instructions within the file to change that.

The *certs/* directory is where you would put all of you SSL certificates.