import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from core.utils import get_next_unique_model_value


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emp_id = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex='/^PSI-\d{4}$/',
                message='Employee ID must be Alphanumeric',
                code='invalid_emp_id'
            ),
        ]
    )

    def save(self, *args, **kwargs):
        if not self.username:
            name = self.first_name.lower() + self.last_name.lower()
            self.username = get_next_unique_model_value(name, self.__class__, "username", 150)

        super(User, self).save(*args, **kwargs)
    
    @property
    def name(self):
        """
        Returns user's name based on the first/last names.
        """
        return f"{self.first_name} {self.last_name}"


class ToolsChoices(models.TextChoices):
    PYATS = 'pyats', _('pyATS')
    XPRESSO = 'xpresso', _('Xpresso')
    EARMS = 'earms', _('Earms')
    TRADE = 'trade', _('Trade')
    LAAS = 'laas', _('LaaS')
    ADSRSVP = 'adsrsvp', _('ADSRSVP')
    SSR = 'ssr', _('SSR')

class SourceOfTicketChoices(models.TextChoices):
    STS = 'sts', _('STS')
    PIESTACK = 'piestack', _('Piestack')
    GITHUB = 'github', _('Github')
    WEBEX = 'webex', _('Webex')
    MALL = 'mall', _('Mall')

class CategoryChoices(models.TextChoices):
    CONFIGMISS = 'configmiss', _('Config Miss')
    SYSADMIN = 'sysadmin', _('Sys Admin')
    BUGFIX = 'bugfix', _('Bug Fix')
    ENHANCEMENT = 'enhancement', _('Enhancement')
    MONITORING = 'monitoring', _('Monitoring')
    TESTINGONLY = 'testingonly', _('Testing Only')
    DOCUMENTATION = 'documentation', _('Documentation')


class KBDocs(models.Model):
    user = models.ForeignKey(
        User, related_name='kbdocs', on_delete=models.CASCADE 
    )
    name = models.CharField(
        max_length=100, blank=True, null=True
    )
    tools = models.CharField(
        max_length=100, choices=ToolsChoices.choices,
        default=ToolsChoices.PYATS
    )
    reporter = models.CharField(
        max_length=255
    )
    created_datetime = models.DateTimeField(auto_now_add=True)
    closed_datetime = models.DateTimeField()
    source_of_ticket = models.CharField(
        max_length=100, choices=SourceOfTicketChoices.choices,
        default=SourceOfTicketChoices.STS
    )
    ticket_link = models.CharField(
        max_length=255
    )
    issue_type = models.CharField(
        max_length=100
    )
    issue_title = models.TextField()
    issue_description = models.TextField()
    category = models.CharField(
        max_length=100, choices=CategoryChoices.choices,
        default=CategoryChoices.SYSADMIN
    )
    help_links = models.TextField(blank=True, null=True)
    resolutions = models.TextField()
    workaround = models.TextField()
    others = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    udpated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "KB Docs"
        verbose_name = "KB Docs"
    
    def __str__(self):
        return f"{self.tools} - {self.issue_type} - {self.issue_title}"
