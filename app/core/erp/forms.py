from datetime import datetime

from django.forms import *

from core.erp.models import Categoria, Producto, Cliente, Venta, Area, Bodega, Tipo_Contrato, Puesto, Empleado, \
    Contrato, Indicador, Ingreso_Indicadores, Pedido


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre_categoria'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre_categoria': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre de categoría',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class AreaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        # self.fields['area'].widget.attrs['autofocus'] = True

    class Meta:
        model = Area
        fields = '__all__'
        widgets = {
            'nombre_area': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre de área',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class BodegaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre_bodega'].widget.attrs['autofocus'] = True

    class Meta:
        model = Bodega
        fields = '__all__'
        widgets = {
            'nombre_bodega': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre de bodega nueva',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TContraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['tipo_contrato'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tipo_Contrato
        fields = '__all__'
        widgets = {
            'tipo_contrato': TextInput(
                attrs={
                    'placeholder': 'Ingrese nuevo tipo de contrato',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PuestoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['puesto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Puesto
        fields = '__all__'
        widgets = {
            'puesto': TextInput(
                attrs={
                    'placeholder': 'Ingrese nuevo puesto',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class IndiForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre_indicador'].widget.attrs['autofocus'] = True

    class Meta:
        model = Indicador
        fields = '__all__'
        widgets = {
            'nombre_indicador': TextInput(
                attrs={
                    'placeholder': 'Ingrese nuevo inidicador de rendimiento',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EmpleadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombres del empleado',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese apellidos del empleado',
                }
            ),
            'dpi': TextInput(
                attrs={
                    'placeholder': 'Ingrese DPI del empleado',
                }
            ),

            'fecha_nacimiento': DateInput(format='%Y-%m-%d',
                                       attrs={
                                           'value': datetime.now().strftime('%Y-%m-%d'),
                                       }
                                       ),

            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese dirección del empleado',
                }
            ),

            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese teléfono del cliente',
                }
            ),
            'gender': Select()

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class ContratoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['fecha'].widget.attrs['autofocus'] = True
        self.fields['tipo'].widget.attrs['class'] = 'form-control select2'
        self.fields['puesto'].widget.attrs['class'] = 'form-control select2'
        self.fields['empleado'].widget.attrs['class'] = 'form-control select2'
        self.fields['area'].widget.attrs['class'] = 'form-control select2'
        # self.fields['fecha_inicio'].widget.attrs['class'] = 'form-control select2'
        self.fields['salario_base'].widget.attrs['style'] = 'width: 100%'
        self.fields['salario_bonificacion'].widget.attrs['style'] = 'width: 100%'



    class Meta:
        model = Contrato
        fields = '__all__'
        widgets = {

            'fecha': DateInput(format='%Y-%m-%d',
                                     attrs={
                                         'value': datetime.now().strftime('%Y-%m-%d'),
                                         'autocomplete': 'off',
                                         'class': 'form-control datetimepicker-input',
                                         'id': 'fecha',
                                         'data-target': '#fecha',
                                         'data-toggle': 'datetimepicker'
                                     }
                                     ),
# selecciona cliente
            'tipo': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

            'puesto': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

            'empleado': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

            'area': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

            # fecha factura
            'fecha_inicio': DateInput(format='%Y-%m-%d',
                                       attrs={
                                            'value': datetime.now().strftime('%Y-%m-%d'),
                                           'autocomplete': 'off',
                                           'class': 'form-control datetimepicker-input',
                                           'id': 'fecha_inicio',
                                           'data-target': '#fecha_inicio',
                                           'data-toggle': 'datetimepicker'
                                       }
            ),

# para quitar flechitas de text
            'salario_base': TextInput(attrs={
                # 'readonly': True,
                'class': 'form-control',
            }),

            'salario_bonificacion': TextInput(attrs={
                # 'readonly': True,
                'class': 'form-control',
            }),


        }


class IngresoIndicadorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        # self.fields['fecha'].widget.attrs['autofocus'] = True
        self.fields['indicador'].widget.attrs['class'] = 'form-control select2'
        self.fields['empleado'].widget.attrs['class'] = 'form-control select2'

        self.fields['valor'].widget.attrs['style'] = 'width: 100%'



    class Meta:
        model = Ingreso_Indicadores
        fields = '__all__'
        widgets = {

            'fecha': DateInput(format='%Y-%m-%d',
                                       attrs={
                                            'value': datetime.now().strftime('%Y-%m-%d'),
                                           'autocomplete': 'off',
                                           'class': 'form-control datetimepicker-input',
                                           'id': 'fecha_indicador',
                                           'data-target': '#fecha_indicador',
                                           'data-toggle': 'datetimepicker'
                                     }
                                     ),
# selecciona cliente
            'indicador': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

            'empleado': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

           'valor': TextInput(attrs={
                # 'readonly': True,
                'class': 'form-control',
            }),


        }


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'categoria': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombres del cliente',
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese apellidos del cliente',
                }
            ),
            'nit': TextInput(
                attrs={
                    'placeholder': 'Ingrese NIT del cliente',
                }
            ),

            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese dirección del cliente',
                }
            ),

            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese teléfono del cliente',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class PedidoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['cliente'].widget.attrs['autofocus'] = True
        self.fields['cliente'].widget.attrs['class'] = 'form-control select2'
        self.fields['cliente'].widget.attrs['style'] = 'width: 100%'

    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            # selecciona cliente
            'cliente': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

            # fecha factura
            'fecha': DateInput(format='%Y-%m-%d',
                                     attrs={
                                         'value': datetime.now().strftime('%Y-%m-%d'),
                                         'autocomplete': 'off',
                                         'class': 'form-control datetimepicker-input',
                                         'id': 'date_joined',
                                         'data-target': '#date_joined',
                                         'data-toggle': 'datetimepicker'
                                     }
                                     ),

            # para quitar flechitas de text
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),

            'iva': TextInput(attrs={

            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),

        }

class VentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['cliente'].widget.attrs['autofocus'] = True
        self.fields['cliente'].widget.attrs['class'] = 'form-control select2'
        self.fields['cliente'].widget.attrs['style'] = 'width: 100%'



    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
# selecciona cliente
            'cliente': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                }
            ),

# fecha factura
            'fecha': DateInput(format='%Y-%m-%d',
                                       attrs={
                                            'value': datetime.now().strftime('%Y-%m-%d'),
                                           'autocomplete': 'off',
                                           'class': 'form-control datetimepicker-input',
                                           'id': 'date_joined',
                                           'data-target': '#date_joined',
                                           'data-toggle': 'datetimepicker'
                                       }
            ),

# para quitar flechitas de text
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),

            'iva': TextInput(attrs={

            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),




        }

class TestForm(Form):
    categories = ModelChoiceField(queryset=Categoria.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))