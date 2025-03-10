
class SQLQuery:
    def __init__(self, query, params=(),message=''):
        self.query = query
        self.params = params
        self.message = message


def insert_into_text_class_query(params=()):
    return SQLQuery("INSERT INTO text_class (label, text) VALUES (?, ?)", params)
