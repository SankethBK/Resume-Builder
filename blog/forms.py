from django import forms

class JobInviteCreateForm(forms.Form):
    title = forms.CharField(max_length = 250, required = True)
    tags = forms.CharField(max_length = 200, required = True)
    content = forms.CharField(widget = forms.Textarea)