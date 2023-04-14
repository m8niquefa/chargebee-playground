import chargebee
from chargebee.api_error import InvalidRequestError


def create_customer(customer_as_dict: dict):
    result = chargebee.Customer.create(customer_as_dict)
    customer = result.customer
    # card = result.card # Cards are deprecated
    return vars(customer)


def get_customer_count():
    # default limit is 10, and maximum limit is 100
    entries = chargebee.Customer.list({"limit": 100})
    return len(entries)


def get_customer_fields():
    entries = chargebee.Customer.list({"limit": 1})
    return vars(entries)["response"][0]["customer"].keys()


def get_customer_by_email(email_to_find: str):
    print("NOTE: This only works if there are 100 customers or less.")
    entries = chargebee.Customer.list({"limit": 100})
    customer_list = vars(entries)["response"]
    if customer_list is None:
        print("No customers found.")
        return None
    for customer in customer_list:
        if customer["customer"]["email"] == email_to_find:
            return customer["customer"]
    print(f"Customer with email {email_to_find} not found.")
    return None


def get_all_customers_emails():
    print("NOTE: This only works if there are 100 customers or less.")
    entries = chargebee.Customer.list({"limit": 100})
    customer_list = vars(entries)["response"]
    return [instance["customer"]["email"] for instance in customer_list]


def get_customer_by_id(id_to_find: str):
    print("NOTE: This only works if there are 100 customers or less.")
    try:
        result = chargebee.Customer.retrieve(id_to_find)
        return vars(result.customer)
    except InvalidRequestError as e:
        print(f"Customer with id {id_to_find} not found.")
        print("Error message: " + str(e))
        return None
