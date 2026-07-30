import pandas as pd
from sqlalchemy import text
from loader import get_engine


def extract_bronze():
    """
    Read podcast metadata from the Bronze layer.
    """
    engine = get_engine()

    query = """
    SELECT *
    FROM bronze.podcast_metadata
    """

    return pd.read_sql(query, engine)


def clean_data(df):
    """
    Clean podcast metadata.
    """

    # Remove duplicate episodes
    df = df.drop_duplicates(subset=["episode_id"])

    # Convert published to datetime
    df["published"] = pd.to_datetime(df["published"], errors="coerce")

    # Fill missing authors
    df["author"] = df["author"].fillna("Unknown")

    # Remove leading/trailing spaces
    df["title"] = df["title"].str.strip()
    df["podcast_title"] = df["podcast_title"].str.strip()

    return df


def load_silver(df):
    """
    Load cleaned data into the Silver layer.
    """
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE silver.podcast_metadata"))

    df.to_sql(
        name="podcast_metadata",
        con=engine,
        schema="silver",
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} records into silver.podcast_metadata")


def main():

    bronze_df = extract_bronze()

    silver_df = clean_data(bronze_df)

    load_silver(silver_df)


if __name__ == "__main__":
    main()