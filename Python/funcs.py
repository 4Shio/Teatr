from alchemys import engine,meta_data

def con(engine,stmt):
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()