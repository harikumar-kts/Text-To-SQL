import pyodbc
from langchain_core.tools import tool
from src.entity.entity_config import DatabaseConfig
from langchain_community.utilities.sql_database import SQLDatabase


class Database:

    @staticmethod
    def client_initialization(db_config: DatabaseConfig):
        # uri = (
        #     f'mssql+pyodbc://{db_config.host}/'
        #     f'{db_config.name}?driver={db_config.odbc_driver}'
        #     f'&TrustServerCertificate={db_config.trusted_server_certificate}'
        #     f'&Encrypt={db_config.encrypt}'
        # )
        uri = 'mssql+pyodbc://localhost/TPMS?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no'
        return SQLDatabase.from_uri(uri)
    
@tool
def query_execution(db_client: SQLDatabase, query: str):
    """Run the SQL Query using client connection"""
    return db_client.run(query, include_columns=True)

@tool
def load_base64_attachment(projects):
    """Read the base64 file from SQL table"""
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'Server=localhost;'       
        'Database=TPMS;'           
        'Port=1433;'               
        'Trusted_Connection=yes;'  
        'TrustServerCertificate=yes;'
        'Encrypt=no'
    )
    cursor = cnxn.cursor()
    attachment_base64 = list()

    pzInsKeys_str = ",".join([f"'{key}'" for key in projects])
    sql_query = f"SELECT pxAttachName, pyAttachStream FROM pc_data_workattach WHERE pzInsKey IN ({pzInsKeys_str});"

    cursor.execute(sql_query) 

    rows = cursor.fetchall()

    for row in rows:
        pxAttachName, pyAttachStream = row
        attachment_base64.append({"pxAttachName": pxAttachName, "pyAttachStream": pyAttachStream})

    cursor.close()
    cnxn.close()

    return attachment_base64


    