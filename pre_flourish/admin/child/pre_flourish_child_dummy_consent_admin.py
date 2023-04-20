from django.conf import settings
from django.contrib import admin
from django.shortcuts import reverse
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
    ModelAdminReplaceLabelTextMixin)
from edc_model_admin import audit_fieldset_tuple

from .exportaction_mixin import ExportActionMixin
from ...admin_site import pre_flourish_admin
from ...forms import PreFlourishChildDummySubjectConsentForm
from ...models import PreFlourishChildDummySubjectConsent


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        url =  settings.DASHBOARD_URL_NAMES.get('pre_flourish_subject_dashboard_url')
        
        child_subject_identifier = request.POST.get('subject_identifier', None)
        
        if child_subject_identifier:

            return reverse(url, args=[child_subject_identifier[:17],])
        
        else:
            return super().redirect_url(request, obj, post_url_continue)


@admin.register(PreFlourishChildDummySubjectConsent, site=pre_flourish_admin)
class PreFlourishChildDummySubjectConsentAdmin(
        ModelAdminMixin, admin.ModelAdmin):

    form = PreFlourishChildDummySubjectConsentForm
    
    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'dob',
                'identity',
                'consent_datetime'),
            }),
        audit_fieldset_tuple)
    search_fields = ('subject_identifier', 'dob',)
    
