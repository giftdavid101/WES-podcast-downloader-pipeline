import feedparser
from pprint import pprint
import pandas as pd

RSS_FEED = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/96c5c41e-0bc8-4661-b184-ae32006cd726/d623ef0b-3fee-4c26-b815-ae32006cd739/podcast.rss"



def fetch_feed():
    """
    Fetch and parse the podcast RSS feed.
    """
    feed = feedparser.parse(RSS_FEED)
    return feed



def main():
    feed = fetch_feed()

    episodes = extract_metadata(feed)

    print(episodes[:2])   # Just for testing
# feed = feedparser.parse(RSS_FEED)

# episode = feed.entries[0]

# episodes = []

# for episode in feed.entries:

#     episode_data = {
#         "episode_id": episode.get("id"),
#         "title": episode.get("title"),
#         "published": episode.get("published"),
#         "duration": episode.get("itunes_duration"),
#         "summary": episode.get("summary"),
#         "episode_link": episode.get("link"),
#         "image_url": episode.get("image", {}).get("href"),
#         "audio_url": (
#             episode.get("media_content", [{}])[0].get("url")
#             if episode.get("media_content")
#             else None
#         )
#     }

#     episodes.append(episode_data)

df = pd.DataFrame(episodes)

print(df.head())
print(df.shape)

# pprint(episode)

# import feedparser

# RSS_FEED = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/96c5c41e-0bc8-4661-b184-ae32006cd726/d623ef0b-3fee-4c26-b815-ae32006cd739/podcast.rss"

# feed = feedparser.parse(RSS_FEED)

# print("Bozo:", feed.bozo)
# print("Entries:", len(feed.entries))

# if feed.bozo:
#     print("Error:", feed.bozo_exception)