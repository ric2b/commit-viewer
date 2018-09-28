import uuid


def url_uuid(url: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, url)
