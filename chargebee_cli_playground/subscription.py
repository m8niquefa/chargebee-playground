import chargebee
from pprint import pprint
from chargebee_cli_playground.customer import get_customer_by_id


def create_subscription_from_customer(items_as_dict: dict, customer_as_dict: dict):
    print("Creating subscription from customer with the following items:")
    print("Customer:")
    pprint(customer_as_dict)
    print("Items:")
    pprint(items_as_dict)
    customer_id = customer_as_dict["id"]
    print(f"Customer ID to create the subscription {customer_id}:\n")
    result = chargebee.Subscription.create_with_items(customer_id, items_as_dict)
    return result


def create_subscription(items_as_dict: dict, customer_id: str):
    customer = get_customer_by_id(customer_id)
    if customer is None:
        print("Customer not found.")
        return None
    print(f"Customer with id {customer_id} found. Creating subscription with the following items:")
    pprint(items_as_dict)
    result = chargebee.Subscription.create_with_items(customer_id, items_as_dict)
    return result


def get_subscription_count():
    # default limit is 10, and maximum limit is 100
    entries = chargebee.Subscription.list({"limit": 100})
    return len(entries)


def get_subscription_fields():
    entries = chargebee.Subscription.list({"limit": 1})
    return vars(entries)["response"][0]["subscription"].keys()


def get_subscription_by_id(id_to_find: str):
    print("NOTE: This only works if there are 100 subscription or less.")
    result = chargebee.Subscription.retrieve(id_to_find)
    return vars(result.subscription)


def get_all_subscription_ids():
    print("NOTE: This only works if there are 100 subscription or less.")
    entries = chargebee.Subscription.list({"limit": 100})
    subscription_list = vars(entries)["response"]
    return [instance["subscription"]["id"] for instance in subscription_list]
