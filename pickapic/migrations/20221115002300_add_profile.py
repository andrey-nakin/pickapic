def upgrade(connection):
    # connection is a plain old sqlite3 database connection
    sql = """
        CREATE TABLE profile
        ( 
            id   INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE profile')
