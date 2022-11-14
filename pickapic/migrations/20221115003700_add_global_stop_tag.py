def upgrade(connection):
    sql = """
        CREATE TABLE global_stop_tag
        ( 
            name TEXT NOT NULL UNIQUE
        ) 
        """
    connection.execute(sql)
    connection.commit()


def downgrade(connection):
    connection.execute('DROP TABLE global_stop_tag')
