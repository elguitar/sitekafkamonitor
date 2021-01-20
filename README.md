# Sitekafkamonitor

Close to the coolest thing ever! Monitors your sites and stores them to Kafka and then to Postgres

## Installation

No installation currently available. Install the dependencies (`pip`) with:
```shell
make installdeps
```

## Usage

### The monitor

```shell
make startmonitor
```

### The databasewriter

```shell
make startwriter
```

## Tests

Unit tests implemented in pytest. Run by using:

```shell
make test
```

## TODO

- [] Test Kafka connection
- [] Test Postgres connection
- [] Add integration tests
- [] Separate requirements.txt to the separate folders
- [] Dockerize
- [] Add CI
- [] Add infrastructure automation
