# forms.py
from django import forms

class SalesOrderImportForm(forms.Form):
    file = forms.FileField(label="Upload Spreadsheet (.xlsx or .csv)")
