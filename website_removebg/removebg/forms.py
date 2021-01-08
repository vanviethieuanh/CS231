from django import forms

class get_link(forms.Form):
    obj_link = forms.CharField(max_length=500)
    bg_link = forms.CharField(max_length=500)
