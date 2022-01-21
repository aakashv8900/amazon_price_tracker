import wsl


def check_database_integrity(schema, tables):
    """Check integrity of a database.

    Args:
        schema (wsl.Schema): WSL schema
        tables: A dict mapping each table name defined in the schema to a table
            (a list of rows)
    Raises:
        wsl.IntegrityError: if the integrity check failed.

    This function will check for violations of KEY and REFERENCE constraints.
    """
    assert isinstance(schema, wsl.Schema)
    assert isinstance(tables, dict)

    idx_of = {}  # key name -> key columns (in sorted order) -> row
    keys_of = {}  # table name -> list of (SchemaKey, columns indices, idx)
    fkeys_of = {}  # table name -> list of (SchemaForeignKey, columns indices, idx)

    for table in schema.tables:
        keys_of[table] = []
        fkeys_of[table] = []

    for schemakey in schema.keys.values():
        idx = {}
        idx_of[schemakey.name] = idx
        keys_of[schemakey.table].append((schemakey, schemakey.columns, idx))

    for schemafkey in schema.foreignkeys.values():
        zkey = sorted(zip(schemafkey.refcolumns, schemafkey.columns))
        local = tuple(y for x, y in zkey)
        remote = tuple(x for x, y in zkey)

        found = False
        for candidate_schemakey, candidate_remote, candidate_idx in keys_of[schemafkey.reftable]:
            if remote == candidate_remote:
                assert found == False
                fkeys_of[schemafkey.table].append((schemafkey, local, candidate_idx))
                found = True

        # XXX: This check should be more "static", i.e. at Schema construction
        # time
        if not found:
            raise ValueError('Foreign key "%s" references table "%s", but there is no matching unique key' %(schemafkey.name, schemafkey.reftable))

    for table, rows in tables.items():
        tablekeys = keys_of[table]
        for row in rows:
            for schemakey, cols, idx in tablekeys:
                rowkey = tuple(row[c] for c in cols)
                if idx.setdefault(rowkey, row) is not row:
                    raise wsl.IntegrityError('Table "%s" has row "%s" which violates key "%s"' %(schemakey.table, row, schemakey.name))

    for table, rows in sorted(tables.items()):
        tablefkeys = fkeys_of[table]
        for row in rows:
            for schemafkey, columns, idx in tablefkeys:
                rowkey = tuple(row[c] for c in columns)
                if rowkey not in idx:
                    raise wsl.IntegrityError('Table "%s" has row "%s" which violates foreign key constraint "%s" (no row corresponding to row key "%s" found in foreign table "%s")' %(schemafkey.table, row, schemafkey.name, rowkey, schemafkey.reftable))
