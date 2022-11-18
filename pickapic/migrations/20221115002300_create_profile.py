def upgrade(connection):
    sql = """
        CREATE TABLE profile
        ( 
            id          INTEGER PRIMARY KEY AUTOINCREMENT, 
            parent_id   INTEGER NULL, 
            name        TEXT NOT NULL,
            UNIQUE(name),
            FOREIGN KEY(parent_id) REFERENCES profile(id)
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE profile')
