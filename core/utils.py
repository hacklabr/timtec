import os
import hashlib
from django.utils.deconstruct import deconstructible


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
