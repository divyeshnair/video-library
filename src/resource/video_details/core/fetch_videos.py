import sqlalchemy
from apiclient.discovery import build
from datetime import datetime, timedelta
from typing import List, Dict
import logging
from extensions import db, scheduler
from config import YOUTUBE_KEYS, SCHEDULER_INTERVAL
from src.resource.video_details.models import Videos

youtube_conn = None


def get_timeframe():
    """
    Fetch content from the youtube as per the earliest timestamp present
    in the database. Get the videos between a certain time frame.
    The logic here is to get the videos between the earliest timestamp and 1 hour
    previous to the earliest timestamp

    """
    start_time = (datetime.today()  - timedelta(
            hours=2, minutes=0)).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = (datetime.today()  - timedelta(
            hours=1, minutes=0)).strftime('%Y-%m-%dT%H:%M:%SZ')

    latest_published_datetime = db.query(Videos).order_by(
        Videos.publish_date_timestamp.asc()).first()
    if latest_published_datetime:
        start_time = (latest_published_datetime.publish_date_timestamp - timedelta(
            hours=1, minutes=0)).strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time = latest_published_datetime.publish_date_timestamp.strftime(
                '%Y-%m-%dT%H:%M:%SZ')

    return start_time, end_time


def initialise_youtube_conn():
    """
    Initialise youtube connection
    """

    global youtube_conn
    if len(YOUTUBE_KEYS) > 0:
        youtube_key = YOUTUBE_KEYS.pop()
        youtube_conn = build('youtube', 'v3',
                             developerKey=youtube_key)
        return
    logging.warning("No credentials available for scraping youtube")


def fetch_youtube_content():
    """
    Fetch youtube content.
    If the connection is not established then re establish the connection
    """

    global youtube_conn
    if youtube_conn:
        start_time, end_time = get_timeframe()
        return youtube_conn.search().list(
            part='snippet',
            publishedAfter=start_time,
            publishedBefore=end_time)

    else:
        initialise_youtube_conn()
        return None


def format_video_details(data: List):
    video_data = [dict(
        title=video.title,
        description=video.description,
        publish_date_timestamp=video.publish_date_timestamp.strftime(
            "%m/%d/%Y, %H:%M:%S"),
        thumbnail_url=video.thumbnail_url
    ) for video in data]

    return video_data


def store_video_details(data: Dict):
    """
    Store the videos in the Videos table

    """
    for videos in data.get("items"):
        snippet = videos.get("snippet")
        video_details = dict(
            video_id=videos.get("id").get("videoId"),
            title=snippet.get("title"),
            description=snippet.get("description"),
            publish_date_timestamp=datetime.strptime(
                snippet.get("publishedAt"), "%Y-%m-%dT%H:%M:%SZ"),
            thumbnail_url=snippet.get("thumbnails").get("default").get(
                "url")
        )
        obj = Videos(**video_details)
        db.add(obj)
        db.flush()
        logging.info(f"Video Id ={videos.get('id').get('videoId')} "
                     "was stored in the database")


@scheduler.task('interval', id='youtube_scrape',
                seconds=SCHEDULER_INTERVAL)
def scrape_videos():
    """
    Execute scraping the youtube and handle scenarios like - 1
    1. If the database has the video id already available
    2. If the quota of the api key has exceeded.
    """
    youtube_content = fetch_youtube_content()
    if youtube_content:
        try:

            res = youtube_content.execute()
            if res:
                store_video_details(res)
        except sqlalchemy.exc.IntegrityError as e:
            db.rollback()
            logging.error("Duplicate video found")

        except Exception as e:
            logging.error(
                f"Youtube API response status code - {e.status_code}")
            if e.status_code == 403:
                global youtube_conn
                youtube_conn = None
                initialise_youtube_conn()

        db.commit()
