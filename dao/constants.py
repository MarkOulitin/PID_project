db_name = 'db.sqlite'

plc_create_statement = """
        CREATE TABLE IF NOT EXISTS "PLC" (
            "PlcId"	INTEGER,
            "PlcPath"	INTEGER UNIQUE,
            PRIMARY KEY("PlcId" AUTOINCREMENT)
        )
    """

requests_create_statement = """
        CREATE TABLE IF NOT EXISTS "Requests" (
            "id"	TEXT,
            "\ValuePath"	TEXT,
            "ValueMin"	REAL,
            "ValueMax"	REAL,
            "SetPointPath"	TEXT,
            "SetPointMin"	REAL,
            "SetPointMax"	REAL,
            "PidPath"	TEXT,
            "PidMin"	REAL,
            "PidMax"	REAL,
            "PidValuePath"	TEXT,
            "PidValueMin"	REAL,
            "PidValueMax"	REAL,
            "P"	REAL,
            "I"	REAL,
            "D"	REAL,
            "SimulationMinutes"	REAL,
            "SimulationSeconds"	BLOB,
            PRIMARY KEY("id")
        )
    """

samples_create_statement = """
        CREATE TABLE "Samples" (
            "SampleId"	INTEGER,
            "PlcId"	INTEGER,
            "ProcessValue"	REAL,
            "PidValue"	REAL,
            "SetPoint"	TEXT,
            "Timestamp"	INTEGER,
            "P"	REAL,
            "I"	REAL,
            "D"	REAL,
            FOREIGN KEY("PlcId") REFERENCES "PLC"("PlcId"),
            PRIMARY KEY("SampleId" AUTOINCREMENT)
        );
    """