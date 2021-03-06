import psycopg2

import options

class PostgresClient:
    """Simple wrapper around Postgresql connection"""

    def __init__(self):

        self.connection = psycopg2.connect(host=options.db_host,
                                           port=options.db_port,
                                           dbname=options.db_name,
                                           user=options.db_user,
                                           password=options.db_password,
                                           sslmode="require",
                                           )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


class MeasurementPostgresClient(PostgresClient):
    """Extends the PostgresClient with app specific methods"""

    def __init__(self):
        super().__init__()

    def create_measurements_table(self):
        """Create the table for measurements"""

        create_clause = """
        CREATE TABLE IF NOT EXISTS measurements (
            id SERIAL,
            url TEXT NOT NULL,
            status SMALLINT,
            latency REAL,
            regex_found BOOLEAN,
            ts TIMESTAMP
        );
        """

        self.cursor.execute(create_clause)
        self.connection.commit()

    def insert_measurement(self, values, autocommit=True):
        """Insert a measurement
        :param values: A tuple of values
        :type values: tuple
        :param autocommit: A bool indicating whether to commit
        :type autocommit: bool, optional"""
        
        insert_clause = """
        INSERT INTO measurements
        (url, status, latency, regex_found, ts)
        VALUES (%s, %s, %s, %s, %s);
        """
        print(values)
        self.cursor.execute(insert_clause, values)
        if autocommit:
            self.connection.commit()

    def batch_insert_measurements(self, list_of_values):
        """Insert many measurements in a single commit

        :param list_of_values: A list of tuple values
        :type list_of_values: list(tuple)"""
        if list_of_values is []:
            return

        for i, values in enumerate(list_of_values):
            # Don't overdo it, commit at least after
            # every 100 inserts.
            # Note: off by one to ignore the initial zero
            autocommit = (i + 1) % 101 == 0
            self.insert_measurement(values, autocommit=autocommit)
        self.connection.commit()
