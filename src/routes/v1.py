from src.resource.video_details.views import GetVideos, SearchVideos
from utils.helper import URLS

urls = [
    URLS(resource=GetVideos,
         endpoint=["videos"],
         name="videos"),

    URLS(resource=SearchVideos,
         endpoint=["videos/search"],
         name="search_videos")

]