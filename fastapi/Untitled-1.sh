https://jeongeunseong.store/openai/ 로 접근했는데 jeongeunseong.store에서 리디렉션한 횟수가 너무 많습니다.라고 뜨는데 어떻게 해결해야할까요?

아래는 fastapi의 로그야.
INFO:     158.179.161.252:34458 - "GET /openai/ HTTP/1.0" 307 Temporary Redirect


아래는 nginx의 설정이야.
server {
        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name www.jeongeunseong.store jeongeunseong.store;

        location / {
                proxy_pass http://jeongeunseong.store:8080;
        }

        location /openai/ {
                proxy_pass http://jeongeunseong.store:8000;
        }

    listen [::]:443 ssl; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/www.jeongeunseong.store/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/www.jeongeunseong.store/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = jeongeunseong.store) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = www.jeongeunseong.store) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


        listen 80 default_server;
        listen [::]:80 default_server;

        server_name www.jeongeunseong.store jeongeunseong.store;
    return 404; # managed by Certbot
}
