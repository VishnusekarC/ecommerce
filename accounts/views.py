
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .utils import verification_token

User = get_user_model()



class ActivateView(View):
    def get_user_from_email_verification_token(self, uidb64, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, OverflowError, ValueError, User.DoesNotExist):
            return None

        if user is not None and verification_token.check_token(user, token):
            return user
        return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(uidb64, token)
        if user is None:
            return HttpResponse('Account Already activated!, Please login')
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('accounts:activate-success'))

class ActivateSuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'activate_success.html')
        
