db_name = 'db.sqlite'

query_request_create_statement = """
        CREATE TABLE IF NOT EXISTS "QueryRequests" (
            "id"	TEXT,
            "PlcPath"	TEXT,
            "P"	REAL,
            "I"	REAL,
            "D"	REAL,
            "SimulationMinutes"	INTEGER,
            "SimulationSeconds"	INTEGER,
            "SetPoint"	TEXT,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY("id")
        )
    """
