from sqlalchemy import create_engine

# DATABASE_URL = "postgresql://airflow:airflow@localhost:5433/airflow"
DATABASE_URL = "postgresql://airflow:airflow@localhost:5433/podcast_pipeline"


def get_engine():
    """
    Create and return a PostgreSQL database engine.
    """
    return create_engine(DATABASE_URL)


def load_to_postgres(df, table_name, schema):
    """
    Load a pandas DataFrame into a PostgreSQL table.
    """
    engine = get_engine()

    df.to_sql(
    name=table_name,
    con=engine,
    schema=schema,
    if_exists="append",
    index=False
    )

    print(f"{table_name} loaded successfully.")

