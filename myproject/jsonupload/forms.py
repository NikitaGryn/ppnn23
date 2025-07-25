from django import forms

class JsonUploadForm(forms.Form):
    json_file = forms.FileField()