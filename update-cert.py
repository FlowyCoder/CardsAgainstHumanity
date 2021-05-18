import re

# linkFile = open("/var/www/vhosts/system/playcah.de/conf/last_nginx.conf")
# linkText = linkFile.read()
linkText = """#ATTENTION!
#
#DO NOT MODIFY THIS FILE BECAUSE IT WAS GENERATED AUTOMATICALLY,
#SO ALL YOUR CHANGES WILL BE LOST THE NEXT TIME THE FILE IS GENERATED.

server {
        listen 178.254.38.252:443 ssl http2;

        server_name playcah.de;
        server_name www.playcah.de;
        server_name ipv4.playcah.de;

        ssl_certificate             /usr/local/psa/var/certificates/scfQubTHy;
        ssl_certificate_key         /usr/local/psa/var/certificates/scfQubTHy;
        ssl_client_certificate      /usr/local/psa/var/certificates/scfTGcyeG;

        client_max_body_size 128m;

        root "/var/www/vhosts/playcah.de/httpdocs";
        access_log "/var/www/vhosts/system/playcah.de/logs/proxy_access_ssl_log";
        error_log "/var/www/vhosts/system/playcah.de/logs/proxy_error_log";

        #extension letsencrypt begin
        location ^~ /.well-known/acme-challenge/ {
                root /var/www/vhosts/default/htdocs;

                types { }
                default_type text/plain;

                satisfy any;
                auth_basic off;
                allow all;

                location ~ ^/\.well-known/acme-challenge.*/\. {
                        deny all;
                }
        }
        #extension letsencrypt end

        location / {
                proxy_pass https://178.254.38.252:7081;
                proxy_set_header Host             $host;
                proxy_set_header X-Real-IP        $remote_addr;
                proxy_set_header X-Forwarded-For  $proxy_add_x_forwarded_for;
                proxy_set_header X-Accel-Internal /internal-nginx-static-location;
                access_log off;

        }

        location /internal-nginx-static-location/ {"""
regex = r"ssl_certificate.*?(/usr/local/psa/var/certificates/.*?)$"
keyFilePath = re.findall(regex, linkText, re.MULTILINE)[0]

keyFile = open(keyFilePath)
keyText = keyFile.read()

privateKeyRegex = r"(-----BEGIN PRIVATE KEY-----(.|\s)*?-----END PRIVATE KEY-----)"
privateKey = re.findall(privateKeyRegex, keyText)[0]
privateCertRegex = r"(-----BEGIN CERTIFICATE-----(.|\s)*?-----END CERTIFICATE-----)"
certificate = re.findall(privateCertRegex, keyText)[0]

pkFileOut = open("private.key", "w")
pkFileOut.write(privateKey)
pkFileOut.close()
certFileOut = open("cert.crt", "w")
certFileOut.write(certificate)
certFileOut.close()