from django import forms

class MailForm(forms.Form):
    query = forms.CharField()
    query_topic = forms.CharField(max_length=50)
    query_heading = forms.CharField(max_length=200)