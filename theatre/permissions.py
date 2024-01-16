from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(
            self,
            request: Request,
            view: GenericAPIView
    ) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or (request.user and request.user.is_staff)
        )
