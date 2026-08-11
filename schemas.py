POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "additionalProperties": False,
}

COMMENT_SCHEMA = {
    "type": "object",
    "required": ["postId", "id", "name", "email", "body"],
    "properties": {
        "postId": {"type": "integer"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "body": {"type": "string"},
    },
    "additionalProperties": False,
}

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "address": {
            "type": "object",
            "required": ["street", "suite", "city", "zipcode", "geo"],
            "properties": {
                "geo": {
                    "type": "object",
                    "required": ["lat", "lng"],
                },
            },
        },
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {
            "type": "object",
            "required": ["name", "catchPhrase", "bs"],
        },
    },
}
