build:
	sudo docker build -t ordermanagement:1.0 .

d.exec:
	sudo docker exec -it compose-ordermanagement-debug bash

d.log:
	sudo docker logs -f -n 100 compose-ordermanagement-debug

d.up:
	sudo docker compose -f docker-compose.debug.yml up -d

d.ps:
	sudo docker compose -f docker-compose.debug.yml ps

d.down:
	sudo docker compose -f docker-compose.debug.yml down



p.exec:
	sudo docker exec -it compose-ordermanagement-product bash

p.log:
	sudo docker logs -f -n 100 compose-ordermanagement-product

p.up:
	sudo docker compose -f docker-compose.product.yml up -d

p.down:
	sudo docker compose -f docker-compose.product.yml down

p.ps:
	sudo docker compose -f docker-compose.product.yml ps

