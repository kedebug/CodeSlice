import wtforms as forms
from wtforms import validators
from django.utils.datastructures import MultiValueDict

class Form(forms.Form):
    def __init__(self, handler=None, obj=None, prefix='', formdata=None, **kwargs):
        if handler:
            formdata = MultiValueDict()
            for name in handler.request.arguments.keys():
                formdata.setlist(name, handler.get_arguments(name))
        forms.Form.__init__(self, formdata, obj=obj, prefix=prefix, **kwargs)

class PostForm(Form):
    title = forms.TextField('Title', validators=[validators.Required()])
    content = forms.TextField('Content', validators=[validators.Required()])
