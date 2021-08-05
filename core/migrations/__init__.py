# import pymysql
# pymysql.install_as_MySQLdb()
from django.db.backends.signals import connection_created


def activate_PRAGMA_sqlite(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        # cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('PRAGMA synchronous = OFF; ')
        cursor.execute('PRAGMA cache_size = n_of_pages;')


connection_created.connect(activate_PRAGMA_sqlite)
