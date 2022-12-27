from django.forms.models import BaseInlineFormSet


class RequiredVariation(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredVariation, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form
