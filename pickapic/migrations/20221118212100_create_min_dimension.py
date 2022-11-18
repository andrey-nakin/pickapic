def upgrade(connection):
    sql = """
        CREATE TABLE min_dimension
        ( 
            profile_id INTEGER NOT NULL,
            width      INTEGER NOT NULL,
            height     INTEGER NOT NULL,
            FOREIGN KEY(profile_id) REFERENCES profile(id)
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE min_dimension')
