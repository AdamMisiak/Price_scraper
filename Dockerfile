FROM python:3.7-alpine

RUN apk --update add bash nano gcc libffi-dev g++ git openssl-dev linux-headers nginx make sed

COPY ./requirements.txt /var/www/requirements.txt
COPY ./price_scraper /var/www/price_scraper
COPY ./price_scraper_app.py /var/www/price_scraper_app.py
COPY ./wsgi.py /var/www/wsgi.py
COPY ./price_scraper.ini /var/www/price_scraper.ini
COPY ./migrations /var/www/migrations
COPY ./price_scraper_nginx /etc/nginx/conf.d/price_scraper_nginx.conf

RUN pip3 install -r /var/www/requirements.txt
RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir /run/nginx
RUN mkdir /var/log/supervisor/
RUN mkdir /var/log/uwsgi/
RUN mkdir /var/run/supervisor

COPY ./supervisord_2.ini /etc/supervisor/conf.d/supervisord_2.ini
COPY ./supervisord.conf /etc/supervisor/supervisord.conf

RUN sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/price_scraper_nginx.conf
CMD ["supervisord"]
