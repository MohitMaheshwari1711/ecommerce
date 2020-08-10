# from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import MarketingPreferenceForm
from .models import MarketingPreference



class MarketingPreferenceUpdateView(UpdateView): # update class to ---> class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'
    # success_message = 'Your email preference have been updated.'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect("/login/?next=/settings/email/")
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj
