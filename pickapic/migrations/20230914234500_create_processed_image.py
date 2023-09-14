def upgrade(connection):
    sql = """
        CREATE TABLE processed_image
        ( 
            profile_id INTEGER NOT NULL,
            image_id TEXT NOT NULL,
            UNIQUE(profile_id, image_id),
            FOREIGN KEY(profile_id) REFERENCES profile(id)
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE processed_image')
