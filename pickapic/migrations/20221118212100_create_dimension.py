def upgrade(connection):
    sql = """
        CREATE TABLE dimension
        ( 
            profile_id INTEGER NOT NULL,
            min_width  INTEGER NOT NULL DEFAULT 0,
            min_height INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(profile_id) REFERENCES profile(id)
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE min_dimension')
