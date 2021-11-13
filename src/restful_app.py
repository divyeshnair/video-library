from flask_cors import CORS
from flask_restful import Api

from src.routes.v1 import urls


def restful_api(app):
    CORS(app, resources={r"/*": {"origins": "*"}})
    api = Api(app, prefix="/")

    for url in urls:
        url.resource.method_decorators = (url.resource.decorators
                                          or []) + \
                                         url.resource.base_decorators \
        if hasattr(url.resource, "base_decorators") else []

        api.add_resource(
            url.resource,
            *url.endpoint,
            endpoint=url.name,
            strict_slashes=False
        )