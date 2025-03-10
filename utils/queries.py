
class SQLQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params


def insert_into_text_class_query(params=()):
    return SQLQuery("INSERT INTO text_class (label, text) VALUES (?, ?)", params)
