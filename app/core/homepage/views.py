from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

class NosotrosView(TemplateView):
    template_name = 'template/index.html'
