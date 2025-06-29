from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import SalesOrder, SalesOrderLines
from .forms import SalesOrderImportForm
import openpyxl

# Customize Admin Panel Titles
admin.site.site_header = "Bright Technology Limited Admin Panel"
admin.site.site_title = "Bright Technology Admin"
admin.site.index_title = "Welcome to Bright Technology Admin"


# Inline admin to show SalesOrderLines within SalesOrder
class SalesOrderLinesInline(admin.TabularInline):
    model = SalesOrderLines
    extra = 1


# Admin class for SalesOrder
@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("order_reference", "customer", "status", "creation_date", "total")
    change_list_template = "admin/salesorder_changelist.html"
    inlines = [SalesOrderLinesInline]  # Attach SalesOrderLines inline
    search_fields = ["order_reference", "customer"]  # For autocomplete

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-orders/", self.admin_site.admin_view(self.import_orders), name="import_orders")
        ]
        return custom_urls + urls

    def import_orders(self, request):
        if request.method == "POST":
            form = SalesOrderImportForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data["file"]
                extension = file.name.split(".")[-1]

                if extension == "xlsx":
                    wb = openpyxl.load_workbook(file)
                    sheet = wb.active
                    for row in sheet.iter_rows(min_row=2, values_only=True):
                        SalesOrder.objects.create(
                            creation_date=row[0],
                            customer=row[1],
                            currency=row[2],
                            order_reference=row[3],
                            salesperson=row[4],
                            status=row[5],
                            total=row[6],
                            primary_contact=row[7],
                            finance_contact=row[8],
                            delivery_address=row[9],
                            invoice_address=row[10],
                            email_address=row[11],
                            delivery_date=row[12],
                            delivery_office_location=row[13],
                            tell_no=row[14],
                            designation=row[15],
                            department=row[16],
                            lpo_confirmation_date=row[17],
                            lpo_date=row[18],
                            lpo_number=row[19],
                            comments=row[20],
                        )
                    self.message_user(request, "Sales orders imported successfully.")
                    return redirect("..")
                else:
                    self.message_user(request, "Unsupported file type.", level="error")
        else:
            form = SalesOrderImportForm()

        return render(request, "admin/salesorder_import.html", {"form": form})


# Admin for managing SalesOrderLines separately with autocomplete
@admin.register(SalesOrderLines)
class SalesOrderLinesAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order_reference']
    list_display = ['order_reference', 'product', 'quantity', 'unit_price', 'cost', 'margin', 'margin_percentage']
    search_fields = ['product']
