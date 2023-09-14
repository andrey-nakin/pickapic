def upgrade(connection):
    sql = """
        CREATE TABLE flickr_min_timestamp
        ( 
            profile_id INTEGER PRIMARY KEY,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY(profile_id) REFERENCES profile(id)
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE flickr_min_timestamp')
