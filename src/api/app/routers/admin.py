"""
    Admin API router.
    Provides API methods (routes) for working with admin stuff.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.services.permissions import Permission
from app.services.request import query_auth_data_from_request
from app.services.api.response import api_success, api_error
from app.services.api.errors import ApiErrorCode
from app.database import crud

from app.database.dependencies import get_db, Session

router = APIRouter()


@router.get("/_admin.getSessionsCounters")
async def method_admin_get_sessions_counters(
    req: Request, db: Session = Depends(get_db)
) -> JSONResponse:
    """Returns sessions counters."""
    auth_data = query_auth_data_from_request(
        req, db, required_permissions=[Permission.admin]
    )
    if not auth_data.user.is_admin:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You are not an administrator. Access denied."
        )
    return api_success(
        {
            "sessions": {
                "time_last_created": str(crud.user_session.get_last(db).time_created),
                "all": crud.user_session.get_count(db),
                "inactive": {
                    "count": crud.user_session.get_inactive_count(db),
                    "grouped": crud.user_session.get_inactive_count_grouped(db),
                },
                "active": {
                    "count": crud.user_session.get_active_count(db),
                    "grouped": crud.user_session.get_active_count_grouped(db),
                },
            }
        }
    )


@router.get("/_admin.getOauthClientsCounters")
async def method_admin_get_oauth_clients_counters(
    req: Request, db: Session = Depends(get_db)
) -> JSONResponse:
    """Returns OAuth clients counters."""
    auth_data = query_auth_data_from_request(
        req, db, required_permissions=[Permission.admin]
    )
    if not auth_data.user.is_admin:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You are not an administrator. Access denied."
        )
    return api_success(
        {
            "oauth_clients": {
                "time_last_created": str(crud.oauth_client.get_last(db).time_created),
                "all": crud.oauth_client.get_count(db),
                "inactive": crud.oauth_client.get_inactive_count(db),
                "active": crud.oauth_client.get_active_count(db),
            }
        }
    )


@router.get("/_admin.getUsersCounters")
async def method_admin_get_users_counters(
    req: Request, db: Session = Depends(get_db)
) -> JSONResponse:
    """Returns users counters."""
    auth_data = query_auth_data_from_request(
        req, db, required_permissions=[Permission.admin]
    )
    if not auth_data.user.is_admin:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You are not an administrator. Access denied."
        )
    return api_success(
        {
            "users": {
                "time_last_created": str(crud.user.get_last(db).time_created),
                "all": crud.user.get_count(db),
                "inactive": crud.user.get_inactive_count(db),
                "active": crud.user.get_active_count(db),
                "vip": crud.user.get_vip_count(db),
                "verified": crud.user.get_verified_count(db),
            }
        }
    )
