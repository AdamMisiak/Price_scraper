run-venv:
	. venv/bin/activate && echo "Running venv"

run-test:
	. pytest -v -s && echo "Running test"


dockerfile-sed:
	sed -i -e 's/$$PORT/'"$$PORT"'/g' /etc/nginx/conf.d/price_scraper_nginx.conf
	cat /etc/nginx/conf.d/price_scraper_nginx.conf
	supervisord