def upgrade(connection):
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
