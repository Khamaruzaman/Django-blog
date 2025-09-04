from django import forms


class BlogSearchForm(forms.Form):
    query = forms.CharField(
        label="Search",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
    )
