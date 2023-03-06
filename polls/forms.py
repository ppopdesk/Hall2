from django import forms

class PollCreationForm(forms.Form):
    poll_title = forms.CharField(required=True)
    poll_description = forms.CharField(required=True)
    poll_question = forms.CharField(required=True,max_length=300)
    poll_deadline = forms.DateField()
    opt1 = forms.CharField(required=True,max_length=300)
    opt2 = forms.CharField(required=True,max_length=300)
