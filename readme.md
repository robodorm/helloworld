usage
------

1. Build an OCI container:
```shell
make build
```

2. Run tests:
```shell
make test_rest
```

Optional you could run app locally:
```shell
make start
```

env vars
------
 - MONGO_URI: connection string to the mongodb (optional; default: stored locally)
 - MONGO_COLLECTION: name of the collection to use (optional; default: helloapp)
 - MONGO_DATABASE: name of the database to use (optional; default: helloapp)
