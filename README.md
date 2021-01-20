# Sitekafkamonitor

Close to the coolest thing ever! Monitors your sites and stores them to Kafka and then to Postgres

## Installation

### Dependencies

No installation currently available. Install the dependencies (`pip`) with:
```shell
git clone git@github.com:elguitar/sitekafkamonitor.git
cd sitekafkamonitor
make installdeps
```

### Secrets

#### Monitor

Drop your `ce.pem`, `service.cert` and `service.key` to `sitemonitor/.secrets/`

Define `KAFKA_HOST`, `KAFKA_PORT` and `KAFKA_TOPIC` in `sitemonitor/.env`

#### Databasewriter

Drop your `ce.pem`, `service.cert`, `service.key` and `database_ca.pem` to `databasewriter/.secrets/`

Define `KAFKA_HOST`, `KAFKA_PORT`, `KAFKA_TOPIC`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` in `databasewriter/.env`

## Usage

For now, the project does not include a `Dockerfile` or anything like that. The `Makefile` makes it a little easier to run common tasks. 

### Monitor

```shell
make startmonitor
```

### Databasewriter

```shell
make startwriter
```

## Tests

Unit tests implemented in pytest. Run by using:

```shell
make test
```

## TODO

- [ ] Test Kafka connection
- [ ] Test Postgres connection
- [ ] Add integration tests
- [ ] Separate requirements.txt to the separate folders
- [ ] Dockerize
- [ ] Add CI
- [ ] Add infrastructure automation
- [ ] Provide a template for `.env`
