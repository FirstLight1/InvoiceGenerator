#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test PDF invoice generation"""

import os
from datetime import datetime, timedelta
from decimal import Decimal

from InvoiceGenerator.api import Address, Client, Provider, Creator, Item, Invoice
from InvoiceGenerator.pdf import SimpleInvoice

def test_invoice_generation():
    """Generate a complete PDF invoice to test the functionality"""

    os.environ['INVOICE_LANG'] = 'sk'

    print("=" * 60)
    print("Testing Invoice PDF Generation")
    print("=" * 60)
    
    # Create provider (company issuing the invoice)
    print("\n1. Creating provider...")
    provider = Provider(
        summary="My Company Ltd.",
        address="123 Business Street",
        city="Prague",
        zip_code="120 00",
        phone="+420 123 456 789",
        email="invoice@mycompany.cz",
        bank_name="Test Bank",
        bank_account="1234567890",
        bank_code="0100",
        vat_id="CZ12345678",
        ir="12345678",
        tax_id="CZ12345678",  # Testing the new parameter
        country="Czech Republic",
    )
    print(f"   ✓ Provider: {provider.summary}")
    print(f"   ✓ Tax ID: {provider.tax_id}")
    
    # Create client (customer receiving the invoice)
    print("\n2. Creating client...")
    client = Client(
        summary="Client Company s.r.o.",
        address="456 Client Avenue",
        city="Brno",
        zip_code="602 00",
        phone="+420 987 654 321",
        email="contact@clientcompany.cz",
        vat_id="CZ87654321",
        ir="87654321",
        country="Czech Republic",
    )
    print(f"   ✓ Client: {client.summary}")
    
    # Create invoice creator
    print("\n3. Creating invoice creator...")
    creator = Creator(
        name="John Accountant"
    )
    print(f"   ✓ Creator: {creator.name}")
    
    # Create invoice
    print("\n4. Creating invoice...")
    invoice = Invoice(client, provider, creator)
    invoice.title = "Invoice"
    invoice.number = "2026001"
    invoice.variable_symbol = "2026001"
    invoice.specific_symbol = "123"
    invoice.date = datetime.now()
    invoice.payback = datetime.now() + timedelta(days=14)
    invoice.taxable_date = datetime.now()
    invoice.currency = "Kč"
    invoice.currency_locale = "cs_CZ.UTF-8"
    invoice.use_tax = True
    print(f"   ✓ Invoice number: {invoice.number}")
    print(f"   ✓ Date: {invoice.date.strftime('%Y-%m-%d')}")
    print(f"   ✓ Due date: {invoice.payback.strftime('%Y-%m-%d')}")
    
    # Add items to invoice
    print("\n5. Adding invoice items...")
    
    item1 = Item(
        count=2,
        price=Decimal('1500.00'),
        description="Web Development Services",
        unit="hours",
        tax=Decimal('0')
    )
    invoice.add_item(item1)
    print(f"   ✓ Item 1: {item1.description} ({item1.count} {item1.unit} @ {item1.price} Kč)")
    
    item2 = Item(
        count=1,
        price=Decimal('5000.00'),
        description="Server Setup and Configuration",
        unit="pcs",
        tax=Decimal('0')
    )
    invoice.add_item(item2)
    print(f"   ✓ Item 2: {item2.description} ({item2.count} {item2.unit} @ {item2.price} Kč)")
    
    item3 = Item(
        count=10,
        price=Decimal('250.00'),
        description="Consulting Hours",
        unit="hours",
        tax=Decimal('0')
    )
    invoice.add_item(item3)
    print(f"   ✓ Item 3: {item3.description} ({item3.count} {item3.unit} @ {item3.price} Kč)")
    
    # Calculate totals
    print("\n6. Calculating totals...")
    print(f"   ✓ Subtotal (without tax): {invoice.price} Kč")
    print(f"   ✓ Total (with tax): {invoice.price_tax} Kč")
    print(f"   ✓ Number of items: {len(invoice.items)}")
    
    # Generate PDF
    print("\n7. Generating PDF...")
    output_file = "/home/lukas-kamen/Documents/projects/python/InvoiceGenerator/test_invoice_output.pdf"
    
    try:
        pdf_invoice = SimpleInvoice(invoice)
        pdf_invoice.gen(output_file, generate_qr_code=False)
        
        # Check if file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"   ✓ PDF generated successfully!")
            print(f"   ✓ File: {output_file}")
            print(f"   ✓ Size: {file_size} bytes")
            return True
        else:
            print(f"   ✗ PDF file was not created")
            return False
            
    except Exception as e:
        print(f"   ✗ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("INVOICE GENERATOR TEST")
    print("=" * 60)
    
    success = test_invoice_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ TEST PASSED - Invoice PDF generated successfully!")
    else:
        print("✗ TEST FAILED - Could not generate invoice PDF")
    print("=" * 60 + "\n")
