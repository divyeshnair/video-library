import logging
import sys

import sqlalchemy as sa
from datetime import datetime
from flask.logging import default_handler

from flask import Flask


class URLS:
    def __init__(self, resource, endpoint, name):
        self.resource = resource
        self.endpoint = endpoint
        self.name = name


class Timestamp(object):
    created = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False,
                        index=True)
    updated = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)