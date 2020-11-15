from django.forms import *

# formulario por componentes para la fecha con rangos
class ReportForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
