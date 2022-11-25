def upgrade(connection):
    sql = """
        CREATE TABLE flickr_license
        ( 
            profile_id INTEGER NOT NULL,
            license_id TEXT NOT NULL,
            UNIQUE(profile_id, license_id),
            FOREIGN KEY(profile_id) REFERENCES profile(id)
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE flickr_license')
