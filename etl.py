import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    This procedure executes COPY into the staging tables.

    INPUTS:
    * cur the cursor variable
    * conn the database connection
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    This procedure executes the insert statements into the final tables.

    INPUTS:
    * cur the cursor variable
    * conn the database connection
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    This procedure creates the database connection.
    Also, it invokes the procedure to load data into the staging tables
        and the procedure to extract, transform and load data into
        the final tables.

    INPUTS:
    * cur the cursor variable
    * conn the database connection
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}"
        .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
