from rest_framework import permissions

from TheSphinx.models import Meeting


class HasMeetingAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user in obj.organizers.all()) or (request.user in obj.attendees.all())


class HasMessageAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user is obj.sender


class IsInSafeMethods(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
