def log_this_find(app, find):
    if find:
        app.logger.info(f"Found {find.name}")
    else:
        app.logger.info(f"Could not find {find.name}")


def upsert(session, app, table, data):
    pass
    # try:
    #     table.get
    #     session.execute(stmt)
    #     session.commit()
    # except Exception as e:
    #     session.rollback()
    #     app.logger.error(e)
