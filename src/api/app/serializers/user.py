"""
    User database model serializer.
"""


import time

from app.database.models.user import User


def serialize(
    user: User,
    *,
    include_email: bool = False,
    include_optional_fields: bool = False,
    include_private_fields: bool = False,
    include_profile_fields: bool = False
):
    """Returns dict object for API response with serialized user data."""
    serialized_user = {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "sex": 0 if user.is_female() else 1,
    }

    if include_profile_fields:
        serialized_user["profile"] = {
            "bio": user.profile_bio,
            "website": user.profile_website,
            "socials": {
                "vk": user.profile_social_username_vk,
                "tg": user.profile_social_username_tg,
                "gh": user.profile_social_username_gh,
            },
            "privacy": {
                "is_public": user.privacy_profile_public,
                "auth_required": user.privacy_profile_require_auth,
            },
        }

    if include_email and include_private_fields:
        serialized_user["email"] = user.email

    if include_optional_fields:
        time_online = user.time_online
        serialized_user["time_created"] = time.mktime(user.time_created.timetuple())
        serialized_user["time_online"] = time.mktime(time_online.timetuple()) if time_online else None
        serialized_user["states"] = {"is_active": user.is_active, "is_vip": user.is_vip}

        if include_private_fields:
            if user.is_admin:
                serialized_user["states"]["is_admin"] = user.is_admin
            serialized_user["states"]["is_confirmed"] = user.is_verified

    return {"user": serialized_user}


serialize_user = serialize
