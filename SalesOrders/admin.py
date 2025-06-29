from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import openpyxl
import csv

from .models import SalesOrder, SalesOrderLines
from .forms import SalesOrderImportForm

admin.site.site_header = "Bright Technology Limited Admin Panel"
admin.site.site_title = "Bright Technology Admin"
admin.site.index_title = "Welcome to Bright Technology Admin"

class SalesOrderLinesInline(admin.TabularInline):
    model = SalesOrderLines
    extra = 1

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("order_reference", "customer", "salesperson", "status", "creation_date", "currency", "total")
    change_list_template = "admin/salesorder_changelist.html"
    inlines = [SalesOrderLinesInline]
    search_fields = ["order_reference", "customer"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-orders/",
                self.admin_site.admin_view(self.import_orders),
                name="SalesOrders_salesorder_import_orders",
            ),
            path(
                "export-orders/",
                self.admin_site.admin_view(self.export_orders),
                name="SalesOrders_salesorder_export_orders",
            ),
            path(
                "<path:object_id>/print-pdf/",
                self.admin_site.admin_view(self.print_pdf_view),
                name="SalesOrders_salesorder_print_pdf",
            ),
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

    def export_orders(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_orders.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Creation Date', 'Customer', 'Currency', 'Order Reference', 'Salesperson',
            'Status', 'Total', 'Primary Contact', 'Finance Contact', 'Delivery Address',
            'Invoice Address', 'Email Address', 'Delivery Date', 'Delivery Office Location',
            'Tell No', 'Designation', 'Department', 'LPO Confirmation Date', 'LPO Date',
            'LPO Number', 'Comments'
        ])

        for order in SalesOrder.objects.all():
            writer.writerow([
                order.creation_date, order.customer, order.currency, order.order_reference,
                order.salesperson, order.status, order.total, order.primary_contact,
                order.finance_contact, order.delivery_address, order.invoice_address,
                order.email_address, order.delivery_date, order.delivery_office_location,
                order.tell_no, order.designation, order.department, order.lpo_confirmation_date,
                order.lpo_date, order.lpo_number, order.comments
            ])

        return response

    def print_pdf_view(self, request, object_id):
        print(f"Looking for SalesOrder with order_reference = {object_id}")
        order = get_object_or_404(SalesOrder, pk=object_id)
        order_lines = order.order_lines.all()

        template = get_template("admin/salesorder_pdf.html")
        html = template.render({"order": order, "order_lines": order_lines})

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="SalesOrder_{order.order_reference}.pdf"'

        pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
        return response

# ✅ Autocomplete and search for order_reference when adding SalesOrderLines
class SalesOrderLinesAdmin(admin.ModelAdmin):
    autocomplete_fields = ["order_reference"]
    search_fields = ["order_reference__order_reference", "order_reference__customer"]

admin.site.register(SalesOrderLines, SalesOrderLinesAdmin)
