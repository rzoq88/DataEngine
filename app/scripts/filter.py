import re
from cassandra.cluster import Cluster

# Establish connection to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra cluster address
session = cluster.connect('dataengine')  # Replace with your keyspace name

# Define compiled regex patterns for field detection
email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
password_pattern = re.compile(r'\b[A-Za-z0-9@#$%^&+=]{8,}\b')
username_pattern = re.compile(r'\b[A-Za-z0-9._%+-]{3,}\b')
ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# Define a function to classify the data fields
def classify_field(field):
    if email_pattern.match(field):
        return 'email'
    elif password_pattern.match(field):
        return 'password'
    elif username_pattern.match(field):
        return 'username'
    elif ip_pattern.match(field):
        return 'ip'
    else:
        return 'unknown'


# # Open and read the text file
# with open('usa.txt', 'r') as file:
#     batch_size = 1000  # Number of rows to insert per batch
#     batch_queries = []
#     for line in file:
#         line = line.strip()
#         fields = line.split(':')

#         # Validate the number of fields
#         if len(fields) >= 9:
#             # Extract and classify each field
#             classified_fields = []
#             for field in fields:
#                 field = field.strip()
#                 field_type = classify_field(field)
#                 classified_fields.append((field, field_type))
#             print(classified_fields)
#             print(fields)
#             # Prepare batch queries
#             for field, field_type in classified_fields:
#                 query = session.prepare("INSERT INTO Data (field, type) VALUES (?, ?)")

#                 batch_queries.append(query.bind((field, field_type)))

#             # Execute batch queries in batches
#             if len(batch_queries) >= batch_size:
#                 batch = session.batch(batch_queries)
#                 session.execute(batch)
#                 batch_queries = []

#     # Insert remaining batch queries
#     if batch_queries:
#         batch = session.batch(batch_queries)
#         session.execute(batch)

# # Close the Cassandra session and cluster connection
# session.shutdown()
# cluster.shutdown()