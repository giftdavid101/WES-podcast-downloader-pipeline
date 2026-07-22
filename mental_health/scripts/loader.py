from sqlalchemy import create_engine

DATABASE_URL = "postgresql://airflow:airflow@localhost:5432/airflow"


def get_engine():
    """
    Create and return a PostgreSQL database engine.
    """
    return create_engine(DATABASE_URL)


def load_to_postgres(df, table_name):
    """
    Load a pandas DataFrame into a PostgreSQL table.
    """
    engine = get_engine()

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} loaded successfully.")

