from django.conf.urls import patterns, url
from .view import SignupCompletionView


urlpatterns = patterns(
    '',
    url(r'^signup-completion/?$', SignupCompletionView.as_view(), name='signup_completion'),
)
