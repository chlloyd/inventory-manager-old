from invmanager import db

def get_all_table_names(ignored_tables=None) -> list:
    """

    Args:
        ignored_tables: The tables to remove from the list. For example tables that the database migration tool makes
        and database internal tables.

    Returns:
        list[str] - A list of all the tables in the tables

    """
    if ignored_tables is None:
        ignored_tables = ['alembic_version', 'sqlite_master']
    table_names = db.engine.table_names()
    assert isinstance(table_names, list)

    for ignored in ignored_tables:
        if ignored in table_names:
            table_names.remove(ignored)

    return table_names
