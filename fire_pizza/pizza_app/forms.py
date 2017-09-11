from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.forms import ModelForm

from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = (
            'name',
            'address',
            'phone',
            'email',
            'message',
        )

    def __init__(self, *args, **kwargs):
        """Add submit to crispy forms form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Make order'))
