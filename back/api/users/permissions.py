from rest_framework import permissions
from .rolesManager import rolesManager


class RolePermission(permissions.BasePermission):
    message = 'Role permission required'

    def has_permission(self, request, view):
        if not hasattr(view, 'requestedRole'):
            return True
        if("ALL" in view.requestedRole):
            return rolesManager.hasPermission(view.requestedRole["ALL"], request.user.role)
        if(request.method in view.requestedRole):
            return rolesManager.hasPermission(view.requestedRole[request.method], request.user.role)
        else:
            return False
