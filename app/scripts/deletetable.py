from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster()  # Replace 'localhost' with your Cassandra cluster address
session = cluster.connect()
# Define the keyspace and table name
keyspace = 'dataengine'
table = 'Data'

# Create the DROP TABLE statement
drop_table_query = f"DROP TABLE {keyspace}.{table}"

# Execute the DROP TABLE statement
session.execute(drop_table_query)
