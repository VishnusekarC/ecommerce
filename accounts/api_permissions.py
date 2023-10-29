
from django.contrib.auth.models import Group
from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            group = Group.objects.get(name="Manager")
            return group in request.user.groups.all()
        except Group.DoesNotExist:
            return False
