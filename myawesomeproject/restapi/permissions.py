from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnlyLesson(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            if request.method in SAFE_METHODS:
                return True
            return obj.teacher.user == request.user


class IsOwnerOrReadOnlyBooking(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            if request.method in SAFE_METHODS:
                return True
            return obj.student.user.id == request.user.id
