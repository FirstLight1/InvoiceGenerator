#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test Slovak translation in invoice generation"""

import os
from datetime import datetime, timedelta
from decimal import Decimal

from InvoiceGenerator.api import Address, Client, Provider, Creator, Item, Invoice
from InvoiceGenerator.pdf import SimpleInvoice

def test_slovak_invoice():
    """Generate a PDF invoice with Slovak language"""
    
    # Set Slovak language
    os.environ["INVOICE_LANG"] = "sk"
    
    print("=" * 60)
    print("Testing Slovak Invoice PDF Generation")
    print("=" * 60)
    
    # Create provider
    print("\n1. Vytváranie dodávateľa...")
    provider = Provider(
        summary="Moja Firma s.r.o.",
        address="Hlavná ulica 123",
        city="Bratislava",
        zip_code="811 01",
        phone="+421 2 1234 5678",
        email="faktura@mojafirma.sk",
        bank_name="Slovenská sporiteľňa",
        bank_account="SK31 1200 0000 1987 4263 7541",
        vat_id="SK2021234567",
        ir="12345678",
        tax_id="SK2021234567",
        country="Slovenská republika",
    )
    print(f"   ✓ Dodávateľ: {provider.summary}")
    print(f"   ✓ IČ DPH: {provider.tax_id}")
    
    # Create client
    print("\n2. Vytváranie odberateľa...")
    client = Client(
        summary="Klientská Firma s.r.o.",
        address="Obchodná 456",
        city="Košice",
        zip_code="040 01",
        phone="+421 55 987 6543",
        email="kontakt@klient.sk",
        vat_id="SK2020987654",
        ir="87654321",
        country="Slovenská republika",
    )
    print(f"   ✓ Odberateľ: {client.summary}")
    
    # Create invoice creator
    print("\n3. Vytváranie tvorcu faktúry...")
    creator = Creator(
        name="Ján Účtovník"
    )
    print(f"   ✓ Vytvoril: {creator.name}")
    
    # Create invoice
    print("\n4. Vytváranie faktúry...")
    invoice = Invoice(client, provider, creator)
    invoice.title = "Faktúra"
    invoice.number = "2026001"
    invoice.variable_symbol = "2026001"
    invoice.specific_symbol = "123"
    invoice.date = datetime.now()
    invoice.payback = datetime.now() + timedelta(days=14)
    invoice.taxable_date = datetime.now()
    invoice.currency = "€"
    invoice.currency_locale = "sk_SK.UTF-8"
    invoice.use_tax = True
    print(f"   ✓ Faktúra č.: {invoice.number}")
    print(f"   ✓ Dátum: {invoice.date.strftime('%Y-%m-%d')}")
    print(f"   ✓ Splatnosť: {invoice.payback.strftime('%Y-%m-%d')}")
    
    # Add items
    print("\n5. Pridávanie položiek faktúry...")
    
    item1 = Item(
        count=2,
        price=Decimal('1500.00'),
        description="Vývoj webových stránok",
        unit="hodín",
        tax=Decimal('0')
    )
    invoice.add_item(item1)
    print(f"   ✓ Položka 1: {item1.description} ({item1.count} {item1.unit} @ {item1.price} €)")
    
    item2 = Item(
        count=1,
        price=Decimal('5000.00'),
        description="Konfigurácia servera",
        unit="ks",
        tax=Decimal('0')
    )
    invoice.add_item(item2)
    print(f"   ✓ Položka 2: {item2.description} ({item2.count} {item2.unit} @ {item2.price} €)")
    
    item3 = Item(
        count=10,
        price=Decimal('250.00'),
        description="Konzultačné hodiny",
        unit="hodín",
        tax=Decimal('0')
    )
    invoice.add_item(item3)
    print(f"   ✓ Položka 3: {item3.description} ({item3.count} {item3.unit} @ {item3.price} €)")
    
    # Calculate totals
    print("\n6. Výpočet súm...")
    print(f"   ✓ Medzisúčet (bez DPH): {invoice.price} €")
    print(f"   ✓ Celkom (s DPH): {invoice.price_tax} €")
    print(f"   ✓ Počet položiek: {len(invoice.items)}")
    
    # Generate PDF
    print("\n7. Generovanie PDF...")
    output_file = "/home/lukas-kamen/Documents/projects/python/InvoiceGenerator/test_invoice_slovak.pdf"
    
    try:
        pdf_invoice = SimpleInvoice(invoice)
        pdf_invoice.gen(output_file, generate_qr_code=False)
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"   ✓ PDF úspešne vygenerované!")
            print(f"   ✓ Súbor: {output_file}")
            print(f"   ✓ Veľkosť: {file_size} bytov")
            return True
        else:
            print(f"   ✗ PDF súbor nebol vytvorený")
            return False
            
    except Exception as e:
        print(f"   ✗ Chyba pri generovaní PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TEST SLOVENSKÉHO PREKLADU FAKTÚRY")
    print("=" * 60)
    
    success = test_slovak_invoice()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ TEST ÚSPEŠNÝ - Slovenská faktúra PDF bola vygenerovaná!")
    else:
        print("✗ TEST ZLYHAL - Nepodarilo sa vygenerovať faktúru PDF")
    print("=" * 60 + "\n")
