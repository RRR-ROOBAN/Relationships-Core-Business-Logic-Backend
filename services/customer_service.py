from models.customer import Customer

def create_customer(db, customer):
    db_customer = Customer(
        name=customer.name,
        email=customer.email
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer