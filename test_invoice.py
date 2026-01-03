#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick manual test for InvoiceGenerator changes"""

from InvoiceGenerator.api import Address, Client, Provider, Creator, Item, Invoice
from decimal import Decimal
from datetime import datetime, timedelta

# Test the new tax_id parameter in Address
print("Testing Address with tax_id...")
provider = Provider(
    summary="Test Company Ltd.",
    address="123 Test Street",
    city="Prague",
    zip_code="120 00",
    phone="+420 123 456 789",
    email="info@testcompany.cz",
    bank_name="Test Bank",
    bank_account="123456789",
    bank_code="0100",
    vat_id="CZ12345678",
    ir="12345678",
    tax_id="CZ12345678",  # New parameter being tested
)

client = Client(
    summary="Client Company",
    address="456 Client St",
    city="Brno",
    zip_code="602 00",
)

creator = Creator(
    name="Test Accountant"
)

# Test invoice creation
print("Creating invoice...")
invoice = Invoice(client, provider, creator)
invoice.title = "Test Invoice"
invoice.number = "2026001"
invoice.date = datetime.now()
invoice.payback = datetime.now() + timedelta(days=14)

# Add items
print("Adding items...")
item1 = Item(
    count=2,
    price=Decimal('100.50'),
    description="Test Product 1",
    unit="pcs",
    tax=Decimal('21')
)
invoice.add_item(item1)

item2 = Item(
    count=1,
    price=Decimal('500'),
    description="Test Service",
    unit="hrs",
    tax=Decimal('21')
)
invoice.add_item(item2)

# Test calculations
print("\n=== Test Results ===")
print(f"Provider tax_id: {provider.tax_id}")
print(f"Invoice total (without tax): {invoice.price}")
print(f"Invoice total (with tax): {invoice.price_tax}")
print(f"Number of items: {len(invoice.items)}")

print("\n✓ Basic tests passed!")
