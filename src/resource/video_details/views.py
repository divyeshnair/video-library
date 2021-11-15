from flask_restful import Resource
from flask import request
from sqlalchemy import or_

from extensions import db
from src.resource.video_details.core.fetch_videos import format_video_details
from src.resource.video_details.models import Videos


class GetVideos(Resource):

    def get(self):
        """
        Return the databse records baseed on the page number and
        the number of records allowed per page.
        """

        request_args = request.args
        page_number = int(request_args.get('page_number', 1))
        records_per_page = int(request_args.get('records_per_page', 10))
        start_rec = (page_number - 1) * records_per_page
        end_rec = page_number * records_per_page
        data = db.query(Videos).order_by(
            Videos.publish_date_timestamp.desc()).all()

        return dict(data=format_video_details(data)[start_rec:end_rec])


class SearchVideos(Resource):

    def post(self):
        """
        Search for the videos with sqlalchemy filter method.
        This can help us with partial string match in the database

        """
        search_query = request.json.get("search_query")
        video_data = Videos.query.filter(
            or_(
                Videos.description.contains(search_query),
                Videos.title.contains(search_query)
            )
        ).all()

        return dict(data=format_video_details(video_data))
