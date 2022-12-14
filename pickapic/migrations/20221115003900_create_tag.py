def upgrade(connection):
    sql = """
        CREATE TABLE tag
        ( 
            profile_id INTEGER NOT NULL,
            name       TEXT NOT NULL,
            is_stop    INTEGER NOT NULL DEFAULT FALSE,
            UNIQUE(profile_id, name),
            FOREIGN KEY(profile_id) REFERENCES profile(id)
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE tag')
