from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import Customer
from app.schemas import CustomerCreate


class CustomerRepository:
    @staticmethod
    def retrieve_by_id(id: int, db: Session):
        """
        Get a specific customer by id
        :param id:
        :param db:
        :return:
        """
        customer = db.query(Customer).filter(Customer.id == id).first()
        return customer

    @staticmethod
    def delete_by_id(id: int, creator_id: int, db: Session):
        """
        Delete customer by id
        :param id:
        :param creator_id:
        :param db:
        :return: Ture if data was deleted else return False if customer not found
        """
        # construct query
        customer_query = db.query(Customer).filter(Customer.id == id, Customer.creator_id==creator_id)

        # if no result is found return false
        if not customer_query.first():
            return False

        # delete customer
        customer_query.delete(synchronize_session=False)

        # commit changes to database
        db.commit()
        return True

    @staticmethod
    def list_all(creator_id: int, db: Session, limit: int = 10, skip: int = 0, first_name_search_phrase: Optional[str] = ""):
        """
        Get all customers using the first_name_search_phrase if entered
        :param creator_id:
        :param db:
        :param first_name_search_phrase:
        :param limit:
        :param skip:
        :return:
        """
        customers = db.query(Customer).filter(Customer.creator_id == creator_id,
                                              Customer.first_name.contains(first_name_search_phrase)). \
            limit(limit).offset(skip).all()
        return customers

    @staticmethod
    def create_new(customer: CustomerCreate, creator_id: int, db: Session):
        """
        Creates a new customer in the database
        :param customer:
        :param creator_id:
        :param db:
        :return:
        """
        customer = Customer(
            first_name=customer.first_name,
            last_name=customer.last_name,
            creator_id=creator_id
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def update_by_id(id: int, customer: Customer, creator_id: int, db: Session):
        """
        Update a customer
        :param id:
        :param customer:
        :param creator_id:
        :param db:
        :return:
        """
        customer_query = db.query(Customer).filter(Customer.id == id, Customer.creator_id == creator_id)

        # customer not found
        if not customer_query.first():
            return False

        customer_query.update(customer, synchronize_session=False)
        db.commit()
        return customer_query.first()
