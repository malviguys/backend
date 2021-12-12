from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsOwnerOrReadOnlyLesson(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            print("SAFE_METHODS")
            print(request.user)
            print(request.method)
            return True
        print("NOT SAFE_METHODS")
        print(request.method)
        print(request.user)
        return obj.teacher.user == request.user


class IsOwnerOrReadOnlyBooking(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.student.user == request.user
