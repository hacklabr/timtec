from accounts.models import TimtecUser
from core.models import Unit
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Portfolio(models.Model):
    """
    Generic class to portfolios
    """
    name = models.CharField(_('Name'), max_length=255)
    youtube_id = models.CharField(_('Youtube_id'), max_length=255)
    url_doc = models.CharField(_('Url_doc'), max_length=255)
    data = models.TextField()
    unit = models.ForeignKey(Unit, verbose_name=_('Unit'), null=True, blank=True, related_name='portfolios')
    comment = models.TextField(_('Comment'), blank=True)

    class Meta:
        verbose_name = _('Portfolio')
        verbose_name_plural = _('Portfolios')
        ordering = [('id')]

    def __unicode__(self):
        return u'%s' % (self.name)


class PortfolioItem(models.Model):

    portfolio = models.ForeignKey(Portfolio, verbose_name=_('Portfolio'))
    user = models.ForeignKey(TimtecUser, verbose_name=_('Student'))
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    youtube_id = models.CharField(_('Youtube_id'), max_length=255)
    url_doc = models.CharField(_('Url_doc'), max_length=255)
    data = models.TextField()
    comment = models.TextField(_('Comment'), blank=True)

    class Meta:
        verbose_name = _('Portfolio item')
        verbose_name_plural = _('Portfolio items')
        ordering = ['timestamp']
