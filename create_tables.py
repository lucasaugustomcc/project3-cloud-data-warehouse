import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    This procedure executes the drop table statements.

    INPUTS:
    * cur the cursor variable
    * conn the database connection
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This procedure executes the create table statements.

    INPUTS:
    * cur the cursor variable
    * conn the database connection
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    This procedure creates and closes the database connection.
    Also, it invokes the create and drop tables procedures.

    INPUTS:
    * cur the cursor variable
    * conn the database connection
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}"
        .format(*config['CLUSTER'].values())
        )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
