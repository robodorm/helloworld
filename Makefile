.PHONY: rebuild build terminate start stop clean restart test_rest test_unit

DATE_A := $(shell date -d "100 day ago" +%F)
DATE_B := $(shell date +%F)


# build a docker container
build:
	-docker build . -t helloapp

clean:
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
# a "restart" is gonna wipe a local database
test_rest: restart
	-sleep 3
	-pyresttest "http://localhost:5123/" helloapp/tests/rest.yml --vars='{"date_a": "$(DATE_A)", "date_b": "$(DATE_B)"}'

