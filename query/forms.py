from django import forms

class QueryForm(forms.Form):
    query = forms.CharField()
    query_topic = forms.CharField()
    query_heading = forms.CharField()