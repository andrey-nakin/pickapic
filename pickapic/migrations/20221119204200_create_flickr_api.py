def upgrade(connection):
    sql = """
        CREATE TABLE flickr_api
        ( 
            profile_id INTEGER PRIMARY KEY,
            api_key    TEXT NOT NULL,
            api_secret TEXT NOT NULL,
            FOREIGN KEY(profile_id) REFERENCES profile(id)
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE flickr_api')
