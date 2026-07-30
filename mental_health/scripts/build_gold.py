import pandas as pd
from sqlalchemy import text
from loader import get_engine


def extract_silver():
    engine = get_engine()

    query = """
    SELECT *
    FROM silver.podcast_metadata
    """

    return pd.read_sql(query, engine)


def build_summary(df):
    """
    Create podcast summary metrics.
    """

    summary = (
        df.groupby("podcast_title")
        .agg(
            total_episodes=("episode_id", "count"),
            first_episode_date=("published", "min"),
            latest_episode_date=("published", "max"),
        )
        .reset_index()
    )

    summary["average_duration_minutes"] = None

    return summary


def load_gold(df):
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE gold.podcast_summary"))

    df.to_sql(
        name="podcast_summary",
        con=engine,
        schema="gold",
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(df)} records into gold.podcast_summary")


def main():

    silver_df = extract_silver()

    gold_df = build_summary(silver_df)

    load_gold(gold_df)


if __name__ == "__main__":
    main()