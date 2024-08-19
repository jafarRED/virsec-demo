import logging
from confluent_kafka import Consumer
import socket
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
import snowflake.connector

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define connection parameters
conn = snowflake.connector.connect(
    user='Jafar',
    password='Indi@1234',
    account='rdxijnh-tw08870',
    warehouse='virsec_warehouse',
    database='VERSECDEMO',
    schema='virsec_schema'
)

# Create a cursor object
cur = conn.cursor()

def oauth_cb(oauth_config):
    auth_token, expiry_ms = MSKAuthTokenProvider.generate_auth_token("ap-south-1")  # Replace with your AWS region
    return auth_token, expiry_ms / 1000  # The library expects expiry in seconds

# Configure the Kafka Consumer
c = Consumer({
    'bootstrap.servers': 'b-2.virsecdemocluster.b2luv7.c3.kafka.ap-south-1.amazonaws.com:9098,b-1.virsecdemocluster.b2luv7.c3.kafka.ap-south-1.amazonaws.com:9098',
    'client.id': socket.gethostname(),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'OAUTHBEARER',
    'oauth_cb': oauth_cb,
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
})

topics_to_tables = {
    'msk-test-topic': 'kafka_table_1',
    'msk-test-topic-2': 'kafka_data_table_2',
    'msk-test-topic-3': 'kafka_data_table_3'
}

c.subscribe(list(topics_to_tables.keys()))

logging.info("Starting consumer!")

try:
    while True:
        msg = c.poll(5)

        if msg is None:
            continue
        if msg.error():
            logging.error(f"Consumer error: {msg.error()}")
            continue

        value = msg.value().decode('utf-8')
        logging.info(f"Received message: {value}")

        topic = msg.topic()
        table = topics_to_tables.get(topic)
        value = value.replace("'", "''")

        data = [(value,)]  # Adjust to match your actual schema

        insert_query = "INSERT INTO {table_name} (message) VALUES (%s)".format(table_name=table)

        try:
            cur.execute(insert_query, data)
            logging.info("Record inserted successfully.")
            conn.commit()

        except Exception as e:
            logging.error(f"Error during insert: {e}")
            conn.rollback()

finally:
    cur.close()
    conn.close()
    c.close()
