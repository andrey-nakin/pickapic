def upgrade(connection):
    sql = """
        CREATE TABLE global_tag
        ( 
            name TEXT NOT NULL UNIQUE
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE global_tag')
