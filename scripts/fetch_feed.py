import os
import feedparser
from pprint import pprint
import pandas as pd
from loader import load_to_postgres

# RSS_FEED = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/96c5c41e-0bc8-4661-b184-ae32006cd726/d623ef0b-3fee-4c26-b815-ae32006cd739/podcast.rss"
# RSS_FEEDS = [
#     "RSS_URL_1",
#     "RSS_URL_2",
#     "RSS_URL_3",
#     "RSS_URL_4",
#     "RSS_URL_5",
#     "RSS_URL_6",
#     "RSS_URL_7",
#     "RSS_URL_8",
# ]


# def fetch_feed():
#     """
#     Fetch and parse the podcast RSS feed.
#     """
#     feed = feedparser.parse(RSS_FEEDS)
#     return feed



# def main():
#     feed = fetch_feed()

#     episodes = extract_metadata(feed)

#     print(episodes[:2])   # Just for testing
# # feed = feedparser.parse(RSS_FEED)

# # episode = feed.entries[0]

# # episodes = []

# # for episode in feed.entries:

# #     episode_data = {
# #         "episode_id": episode.get("id"),
# #         "title": episode.get("title"),
# #         "published": episode.get("published"),
# #         "duration": episode.get("itunes_duration"),
# #         "summary": episode.get("summary"),
# #         "episode_link": episode.get("link"),
# #         "image_url": episode.get("image", {}).get("href"),
# #         "audio_url": (
# #             episode.get("media_content", [{}])[0].get("url")
# #             if episode.get("media_content")
# #             else None
# #         )
# #     }

# #     episodes.append(episode_data)

# # df = pd.DataFrame(episodes)

# # print(df.head())
# # print(df.shape)

# def extract_metadata(feed):
#     """
#     Extract podcast episode metadata from the RSS feed.
#     """

#     episodes = []

#     for episode in feed.entries:

#         episode_data = {
#             "episode_id": episode.get("id"),
#             "title": episode.get("title"),
#             "published": episode.get("published"),
#             "duration": episode.get("itunes_duration"),
#             "summary": episode.get("summary"),
#             "episode_link": episode.get("link"),
#             "image_url": episode.get("image", {}).get("href"),
#             "audio_url": (
#                 episode.get("media_content", [{}])[0].get("url")
#                 if episode.get("media_content")
#                 else None
#             ),
#         }

#         episodes.append(episode_data)

#     return episodes

# def create_dataframe(episodes):
#     """
#     Convert the extracted metadata into a pandas DataFrame.
#     """
#     df = pd.DataFrame(episodes)
#     print(df.shape)

#     return df



# def save_metadata(df):
#     """
#     Save podcast metadata to a CSV file.
#     """

#     output_dir = "data/raw/metadata"
#     os.makedirs(output_dir, exist_ok=True)

#     output_file = os.path.join(output_dir, "podcast_metadata.csv")

#     df.to_csv(output_file, index=False)

#     print(f"Metadata saved to {output_file}")


# def main():

#     feed = fetch_feed()

#     episodes = extract_metadata(feed)

#     df = create_dataframe(episodes)
#     df["podcast_title"] = feed.feed.title

#     # print(df.head())
#     # print(df.shape)
#     save_metadata(df)
#     # load_to_postgres(df)
#     # load_to_postgres(df, "podcast_metadata")
#     load_to_postgres(
#     df=df,
#     table_name="podcast_metadata",
#     schema="bronze"
#     )



# if __name__ == "__main__":
#     main()


# # pprint(episode)

# # import feedparser

# # RSS_FEED = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/96c5c41e-0bc8-4661-b184-ae32006cd726/d623ef0b-3fee-4c26-b815-ae32006cd739/podcast.rss"

# # feed = feedparser.parse(RSS_FEED)

# # print("Bozo:", feed.bozo)
# # print("Entries:", len(feed.entries))

# # if feed.bozo:
# #     print("Error:", feed.bozo_exception)

import os
import feedparser
import pandas as pd

from loader import load_to_postgres
from config import RSS_FEEDS

# ==============================
# RSS FEEDS
# ==============================

RSS_FEEDS = [
    "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/96c5c41e-0bc8-4661-b184-ae32006cd726/d623ef0b-3fee-4c26-b815-ae32006cd739/podcast.rss",
    "https://www.hiddenbrain.org/feed",
    "https://feeds.megaphone.fm/ten-percent-happier",
    "https://feeds.megaphone.fm/feelbetterlivemore",
    "https://feeds.megaphone.fm/therapy-for-black-girls",
    "https://feeds.megaphone.fm/beingwell",
    "https://feeds.megaphone.fm/thepsychologypodcast",
    "https://feeds.simplecast.com/hardcoreselfhelp"
]



# ==============================
# FETCH RSS FEEDS
# ==============================

def fetch_feeds():
    """
    Fetch and parse all podcast RSS feeds.
    """

    feeds = []

    for rss_url in RSS_FEEDS:
        print(f"Fetching: {rss_url}")

        feed = feedparser.parse(rss_url)

        if feed.bozo:
            print(f"Skipping invalid feed: {rss_url}")
            continue

        feeds.append(feed)

    return feeds


# ==============================
# EXTRACT METADATA
# ==============================

def extract_metadata(feeds):
    """
    Extract metadata from all podcast RSS feeds.
    """

    episodes = []

    for feed in feeds:

        podcast_title = feed.feed.get("title")
        podcast_author = feed.feed.get("author")

        for episode in feed.entries:

            episode_data = {

                "episode_id": episode.get("id"),

                "podcast_title": podcast_title,

                "author": podcast_author,

                "title": episode.get("title"),

                "published": episode.get("published"),

                "duration": episode.get("itunes_duration"),

                "summary": episode.get("summary"),

                "episode_link": episode.get("link"),

                "image_url": episode.get("image", {}).get("href"),

                "audio_url": (
                    episode.get("media_content", [{}])[0].get("url")
                    if episode.get("media_content")
                    else None
                ),
            }

            episodes.append(episode_data)

    return episodes


# ==============================
# CREATE DATAFRAME
# ==============================

def create_dataframe(episodes):
    """
    Convert extracted metadata into a pandas DataFrame.
    """

    df = pd.DataFrame(episodes)

    print(f"\nTotal Episodes Loaded: {len(df)}")

    return df


# ==============================
# SAVE CSV
# ==============================

def save_metadata(df):
    """
    Save metadata locally as CSV.
    """

    output_dir = "data/raw/metadata"

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "podcast_metadata.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"Metadata saved to {output_file}")


# ==============================
# MAIN
# ==============================

def main():

    feeds = fetch_feeds()

    episodes = extract_metadata(feeds)

    df = create_dataframe(episodes)

    save_metadata(df)

    load_to_postgres(
        df=df,
        table_name="podcast_metadata",
        schema="bronze"
    )


if __name__ == "__main__":
    main()