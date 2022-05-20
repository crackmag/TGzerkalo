import psycopg2
from psycopg2 import extras
from psycopg2.extensions import AsIs
from config import DATABASE_URL

# Создание таблицы BINDING_ID
def create_table():
    """Creates BINDING_ID table
    """
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS BINDING_ID
            (   id serial primary key not null,
                mirror_message_id bigint not null,
                message_id bigint not null,
                mirror_channel_id bigint not null,
                channel_id bigint not null
            )
            """
        )
        connection.commit()
    except Exception as e:
        print(e)
    cursor.close()
    connection.close()

# Добавление соотвествия идентификаторов
# оригинального и скопированного сообщений
def insert(message):
    """Inserts item into BINDING_ID table

    Args:
        message (dict): Represents row of BINDING_ID table
    """
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    try:
        columns = message.keys()
        values = message.values()
        sql_insert = 'insert into BINDING_ID (%s) values %s'
        cursor.execute(sql_insert, (AsIs(','.join(columns)), tuple(values)))
        connection.commit()
    except Exception as e:
        print(e)
    cursor.close()
    connection.close()

# Поиск значения идентификатора скопированного сообщения
# соответствующему идентификатору оригинального сообщения
def find_by_id(message_id, channel_id):
    """Returns IDs of mirror channels and their messages
    for provided original channel and message IDs

    Args:
        message_id (int): ID of original message
        channel_id (int): ID of original channel

    Returns:
        List[RealDictRow]: Results
    """
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("""
                        SELECT mirror_channel_id, mirror_message_id FROM BINDING_ID
                        WHERE message_id = %s
                        AND channel_id = %s
                        """, (message_id, channel_id, ))
        rows = cursor.fetchone()
        cursor.close()
        connection.close()
        return rows
    except Exception as e:
        print(e)

create_table()
