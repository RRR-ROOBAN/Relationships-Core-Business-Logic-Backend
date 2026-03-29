from models.invoice import Invoice
from models.invoice_item import InvoiceItem


def create_invoice(db, invoice):

    # 🔹 calculate total from items
    items_total = sum(item.quantity * item.price for item in invoice.items)

    # 🔹 final total
    total_amount = items_total + invoice.tax - invoice.discount

    # ❌ prevent invalid amount
    if total_amount <= 0:
        raise ValueError("Total amount must be greater than 0")

    # 🔹 create invoice
    db_invoice = Invoice(
        customer_id=invoice.customer_id,
        tax=invoice.tax,
        discount=invoice.discount,
        due_date=invoice.due_date,
        total_amount=total_amount,
        status="PENDING"
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    # 🔹 add items
    for item in invoice.items:
        db_item = InvoiceItem(
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price,
            invoice_id=db_invoice.id
        )
        db.add(db_item)

    db.commit()

    return db_invoice