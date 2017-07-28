import os
import hashlib
from django.utils.deconstruct import deconstructible
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from braces.views._access import AccessMixin
from django.shortcuts import redirect


@deconstructible
class HashName(object):
    def __init__(self, path, attr):
        self.path = path
        self.attr = attr

    def __call__(self, instance, filename):
        root, ext = os.path.splitext(filename)
        m = hashlib.md5()
        m.update(root.encode('utf-8'))
        name = getattr(instance, self.attr)
        if name:
            m.update(name.encode('utf-8'))
        filename = m.hexdigest() + ext
        # return the whole path to the file
        return os.path.join(self.path, filename)


hash_name = HashName


class AcceptedTermsRequiredMixin(AccessMixin):
    """Verify that the current user has accepted Terms of Service."""
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.accepted_terms and settings.TERMS_ACCEPTANCE_REQUIRED:
            return redirect(reverse_lazy('accept_terms'))
        return super(AcceptedTermsRequiredMixin, self).dispatch(request, *args, **kwargs)
