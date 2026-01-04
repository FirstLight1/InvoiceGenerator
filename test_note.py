#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime, timedelta

# Add the InvoiceGenerator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'InvoiceGenerator'))

from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice

# Set Slovak language
os.environ['INVOICE_LANG'] = 'sk'

# Create client
client = Client(
    summary="Testovací zákazník s.r.o.",
    address="Hlavná 123",
    city="Bratislava",
    zip_code="811 01",
    phone="+421 900 123 456",
    email="zakaznik@example.sk",
    ir="12345678",
    vat_id="SK1234567890",
    tax_id="SK9876543210"
)

# Create provider
provider = Provider(
    summary="Moja firma s.r.o.",
    address="Obchodná 456",
    city="Košice",
    zip_code="040 01",
    phone="+421 900 654 321",
    email="firma@example.sk",
    bank_name="Slovenská sporiteľňa",
    bank_account="1234567890",
    bank_code="0900",
    ir="87654321",
    vat_id="SK0987654321",
    tax_id="SK1234509876"
)

# Create creator
creator = Creator(name="Ján Novák")

# Create invoice
invoice = Invoice(client, provider, creator)
invoice.title = "Faktúra"
invoice.number = "2026001"
invoice.use_tax = True
invoice.currency_locale = 'sk_SK.UTF-8'
invoice.date = datetime.now()
invoice.payback = datetime.now() + timedelta(days=14)
invoice.taxable_date = datetime.now()
invoice.variable_symbol = "2026001"
invoice.paytype = "Bankový prevod"
invoice.iban = "SK89 0900 0000 0001 2345 6789"
invoice.swift = "GIBASKBX"

# Add note at the bottom
invoice.note = "Poznámka: Ďakujeme za vaše podnikanie!\nV prípade otázok nás kontaktujte."

# Add items
item1 = Item(
    count=2,
    price=150.00,
    description="Webový dizajn - úvodná stránka",
    unit="ks",
    tax=20
)

item2 = Item(
    count=5,
    price=80.00,
    description="Programovanie - podstránky",
    unit="hodín",
    tax=20
)

item3 = Item(
    count=1,
    price=250.00,
    description="SEO optimalizácia",
    unit="ks",
    tax=20
)

invoice.add_item(item1)
invoice.add_item(item2)
invoice.add_item(item3)

# Generate PDF
pdf = SimpleInvoice(invoice)
output_file = "test_invoice_with_note.pdf"
pdf.gen(output_file, generate_qr_code=False)

print(f"Invoice with note generated: {output_file}")
print(f"Note content: {invoice.note}")
