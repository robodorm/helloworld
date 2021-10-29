.PHONY: rebuild build terminate start stop restart test_rest test_unit

DATE_A := $(shell date -d "100 day ago" +%F)
DATE_B := $(shell date +%F)


# build a docker container
build:
	-docker build . -t helloapp
	-docker rmi $(docker images -q -f dangling=true)

# rebuild the container
rebuild: terminate
	-docker rm helloapp || true
	-docker rmi helloapp || true
	-docker build . -t helloapp
	-docker rmi $(docker images -q -f dangling=true) || true

#restart a docker container
terminate:
	-docker stop helloapp || true
	-docker rm helloapp || true

start:
	-docker run -d -p 5123:80 --name helloapp helloapp

restart: terminate start

# run rest test
test_rest: restart
	-sleep 3
	-pyresttest "http://localhost:5123/" helloapp/tests/rest.yml --vars='{"date_a": "$(DATE_A)", "date_b": "$(DATE_B)"}'

# run rest test
test_unit:
	-docker exec -it helloapp "cd /app/helloapp/tests && python -m unittest"


#########
# aliases
b: build
s: start
r: restart
t: terminate
rb: rebuild

# tests
tr: test_rest
tu: test_unit

