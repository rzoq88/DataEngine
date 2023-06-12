import pathlib
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection

from . import config

# BASE_DIR = pathlib.Path(__file__).resolve().parent

# settings = config.get_settings()

# ASTRADB_CONNECT_BUNDLE = BASE_DIR / "unencrypted" / "astradb_connect.zip"

# ASTRADB_CLIENT_ID = settings.db_client_id
# ASTRADB_CLIENT_SECRET = settings.db_client_secret

def get_session():
    
    cluster = Cluster()
    session = cluster.connect()
    session.execute("CREATE KEYSPACE IF NOT EXISTS dataEngine WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };")

       
    

    # session.execute("CREATE CUSTOM INDEX  fn_prefix  ON dataengine.Data (email) USING 'org.apache.cassandra.index.sasi.SASIIndex';")
    # session.execute("CREATE CUSTOM INDEX data_email_idx ON dataengine.Data (email) USING 'org.apache.cassandra.index.sasi.SASIIndex' WITH OPTIONS = { 'analyzer_class': 'org.apache.cassandra.index.sasi.analyzer.StandardAnalyzer', 'case_sensitive': 'false'};")
    # print(session.execute('DESCRIBE keyspaces').all())
    # print('hello')
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    return session