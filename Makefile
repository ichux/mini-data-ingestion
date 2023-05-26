# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: mini-data-ingestion help
# help:

.PHONY: help
# help: help				- Please use "make <target>" where <target> is one of
help:
	@grep "^# help\:" Makefile | sed 's/\# help\: //' | sed 's/\# help\://'

.PHONY: b
# help: b 				- build main image
b:
	@docker-compose -p mdi up --build --detach
	@#cd mini_data; docker run --rm --name mini-data-ingestion -p 8005:5000 -it $(docker build -t mini-data-ingestion .)

.PHONY: l
# help: l 				- show logs of the container
l:
	@docker logs -f mdi-app-1

.PHONY: a
# help: a 				- create admin
a:
	@docker exec -i mdi-app-1 flask fab create-admin --username admin --password admin --firstname admin --lastname admin --email admin@example.org