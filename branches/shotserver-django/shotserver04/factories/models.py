from django.db import models
from django.contrib.auth.models import User

class OperatingSystemGroup(models.Model):
    name = models.CharField(maxlength=30)
    maker = models.CharField(maxlength=30)
    def __str__(self): return self.name
    class Admin: pass


class OperatingSystem(models.Model):
    operatingsystemgroup = models.ForeignKey(OperatingSystemGroup)
    distro = models.CharField('distribution', maxlength=30)
    version = models.CharField('version number', maxlength=30)
    codename = models.CharField(maxlength=30, null=True)
    def __str__(self):
        return '%s %s %s (%s)' % (self.operatingsystemgroup.name,
                                  self.distro, self.version, self.codename)
    class Admin: pass


class Factory(models.Model):
    name = models.CharField(maxlength=30)
    admin = models.ForeignKey(User, verbose_name='administrator')
    architecture = models.CharField('hardware architecture', maxlength=30)
    operatingsystem = models.ForeignKey(
        OperatingSystem, verbose_name='operating system')
    created = models.DateTimeField('date created', auto_now_add=True)
    def __str__(self): return self.name
    class Admin:
        fields = (
            (None, {'fields': ('name', 'admin')}),
            ('Platform', {'fields': ('architecture', 'operatingsystem')}),
            )
        list_display = ('name', 'operatingsystem', 'architecture')
    class Meta:
        verbose_name_plural = 'factories'


class ScreenSize(models.Model):
    factory = models.ForeignKey(Factory,
        edit_inline=models.TABULAR, num_in_admin=3)
    width = models.IntegerField(core=True)
    height = models.IntegerField(core=True)
    def __str__(self):
        return '%dx%d' % (self.width, self.height)
    class Meta:
        unique_together = (('factory', 'width', 'height'), )
    class Admin:
        list_display = ('factory', 'width', 'height')