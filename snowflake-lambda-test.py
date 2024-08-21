import logging
import snowflake.connector
from time import sleep

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_snowflake_connection():
    retry_count = 0
    while retry_count < 3:
        try:
            logging.info("Attempting to connect to Snowflake...")
            conn = snowflake.connector.connect(
                user='Jafar',
                password='Indi@1234',
                account='rdxijnh-tw08870',
                warehouse='virsec_warehouse',
                database='VERSECDEMO',
                schema='VIRSEC_SCHEMA'
            )
            logging.info("Connection successful")
            return conn
        except snowflake.connector.errors.OperationalError as e:
            logging.error(f"Snowflake connection failed: {e}")
            retry_count += 1
            sleep(5)  # Wait before retrying

    raise Exception("Failed to connect to Snowflake after multiple attempts.")

def lambda_handler(event, context):
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        # Sample data to insert
        sample_data = [
            ('Message 1',),
            ('Message 2',),
            ('Message 3',)
        ]

        # Query to insert data
        insert_query = "INSERT INTO KAFKA_DATA_TABLE (message) VALUES (%s)"

        # Execute the insert statements
        for data in sample_data:
            cur.execute(insert_query, data)
            logging.info(f"Inserted data: {data}")

        # Commit the transaction
        conn.commit()

        # Return success message
        return {
            'statusCode': 200,
            'body': 'Data inserted successfully'
        }

    except Exception as e:
        logging.error(f"Error during data insertion: {e}")
        return {
            'statusCode': 500,
            'body': f"Error: {e}"
        }

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


############################################################################################

import logging
import snowflake.connector
from time import sleep

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_snowflake_connection():
    try:
        logging.info("Attempting to connect to Snowflake...")
        conn = snowflake.connector.connect(
            user='Jafar',
            password='Indi@1234',
            account='rdxijnh-tw08870',
            warehouse='virsec_warehouse',
            database='VERSECDEMO',
            schema='VIRSEC_SCHEMA'
        )
        logging.info("Connection successful")
        return conn
    except snowflake.connector.errors.OperationalError as e:
        logging.error(f"Snowflake connection failed: {e}")
        raise

def lambda_handler(event, context):
    conn = None
    cur = None
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        # Sample data to insert
        sample_data = [
            ('Message 10',),
            ('Message 12',),
            ('Message 13',)
        ]

        # Query to insert data
        insert_query = "INSERT INTO KAFKA_DATA_TABLE (message) VALUES (%s)"

        # Execute the insert statements
        for data in sample_data:
            cur.execute(insert_query, data)
            logging.info(f"Inserted data: {data}")

        # Commit the transaction
        conn.commit()

        # Return success message
        return {
            'statusCode': 200,
            'body': 'Data inserted successfully'
        }

    except Exception as e:
        logging.error(f"Error during data insertion: {e}")
        return {
            'statusCode': 500,
            'body': f"Error: {e}"
        }

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
