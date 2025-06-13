from django.utils.safestring import SafeString

class BaseFormMixin(object):
    required_css_class = "required"

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
    
class ColumnFormMixin(object):

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", f"<div class='col column-{self.prefix}'>"))