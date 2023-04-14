import os
import json
import argparse
from pprint import pprint
import chargebee
from dotenv import load_dotenv

from chargebee_cli_playground.customer import (
    get_customer_count,
    get_customer_fields,
    get_customer_by_email,
    get_all_customers_emails,
    get_customer_by_id,
    create_customer,
)
from chargebee_cli_playground.subscription import (
    get_subscription_count,
    get_subscription_fields,
    get_subscription_by_id,
    get_all_subscription_ids,
    create_subscription,
    create_subscription_from_customer,
)


def configure():
    load_dotenv()

    CHARGE_BEE_API_KEY = os.environ.get("CHARGE_BEE_API_KEY")
    CHARGE_BEE_URL = os.environ.get("CHARGE_BEE_URL")

    if CHARGE_BEE_API_KEY is None:
        print("Environment variable CHARGE_BEE_API_KEY not found")
        exit()

    if CHARGE_BEE_URL is None:
        print("Environment variable CHARGE_BEE_URL not found")
        exit()

    print("[OK] Load environment variables")
    chargebee.configure(CHARGE_BEE_API_KEY, CHARGE_BEE_URL)
    print("[OK] Configured chargebee")


def print_customer_count(args):
    count = get_customer_count()
    print(f"Customer count: {count} {'' if count <= 100 else ' or more.'}")


def print_subscription_count(args):
    count = get_subscription_count()
    print(f"Subscription count: {count} {'' if count <= 100 else ' or more.'}")


def print_customer_fields(args):
    fields = get_customer_fields()
    for field in fields:
        print(field)


def print_subscription_fields(args):
    fields = get_subscription_fields()
    for field in fields:
        print(field)


def print_customer_by_email(args):
    customer = get_customer_by_email(args.email)
    pprint(customer)


def print_all_customers_emails(args):
    emails = get_all_customers_emails()
    for email in emails:
        print(email)


def print_customer_by_id(args):
    customer = get_customer_by_id(args.id)
    pprint(customer)


def print_subscription_by_id(args):
    subscription = get_subscription_by_id(args.id)
    pprint(subscription)


def print_all_subscription_ids(args):
    subscription_ids = get_all_subscription_ids()
    for id in subscription_ids:
        print(id)


def create_customer_from_file(args):
    with open(args.file, "r") as file:
        data = json.load(file)

    print("Data to use in ChargeBee Customer Creation:\n")
    pprint(data)

    response = create_customer(data)
    print("Response from ChargeBee:\n")
    print(f"response type: {type(response)}\n")
    pprint(vars(response))


def create_subscription_from_file(args):
    with open(args.file, "r") as file:
        data = json.load(file)

    print("Data to use in ChargeBee Subscription Creation:\n")
    pprint(data)

    response = create_subscription(data, args.customer_id)
    print("Response from ChargeBee:\n")
    pprint(vars(response))


def create_chargebee_customer_with_subscription(data_for_customer_creation: dict, subscription_data: dict):
    print("Subscription Data to use in ChargeBee Customer creation:\n")
    print(f"customer_data type: {type(data_for_customer_creation)}\n")
    pprint(data_for_customer_creation)

    created_customer_in_chargebee = create_customer(data_for_customer_creation)
    if created_customer_in_chargebee is None:
        print("Customer creation failed, aborting subscription creation")
        return

    print(f"customer type: {type(created_customer_in_chargebee)}\n")
    customer_as_dict = vars(created_customer_in_chargebee)
    print(f"customer_as_dict type: {type(customer_as_dict)}\n")
    print("Response from ChargeBee on Customer creation:\n")
    pprint(customer_as_dict)

    print("Data to use in ChargeBee Subscription Creation:\n")
    pprint(subscription_data)

    customer_id = customer_as_dict["id"]
    print(f"Customer ID to create the subscription {customer_id}:\n")

    subscription = create_subscription(subscription_data, customer_id)
    print("Response from ChargeBee on subscription creation:\n")
    print(f"subscription type: {type(subscription)}\n")
    subscription_as_dict = vars(subscription)
    print(f"subscription_as_dict type: {type(subscription_as_dict)}\n")
    pprint(subscription_as_dict)


def create_customer_and_subscription(args):
    with open(args.customer_file, "r") as file:
        data_for_customer_creation = json.load(file)

    with open(args.subscription_file, "r") as file:
        subscription_data = json.load(file)

    create_chargebee_customer_with_subscription(data_for_customer_creation, subscription_data)


def main():
    configure()
    parser = argparse.ArgumentParser(description="MachEight Chargebee CLI playground")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("get_customer_count", help="Get customer count")
    subparsers.add_parser("get_subscription_count", help="Get Subscription count")
    subparsers.add_parser("get_customer_fields", help="Get customer fields")
    subparsers.add_parser("get_subscription_fields", help="Get Subscription fields")

    get_customer_by_email_parser = subparsers.add_parser("get_customer_by_email", help="Get customer by email")
    get_customer_by_email_parser.add_argument("--email", help="Email address of the customer to get", required=True)

    subparsers.add_parser("get_all_customers_emails", help="Get all customers emails")

    get_customer_by_id_parser = subparsers.add_parser("get_customer_by_id", help="Get customer by id")
    get_customer_by_id_parser.add_argument("--id", help="Id of the customer to get", required=True)

    get_subscription_by_id_parser = subparsers.add_parser("get_subscription_by_id", help="Get Subscription by id")
    get_subscription_by_id_parser.add_argument("--id", help="Id of the subscription to get", required=True)

    subparsers.add_parser("get_all_subscription_ids", help="Get all subscription ids")

    create_customer_parser = subparsers.add_parser("create_customer", help="Create a customer from a file")
    create_customer_parser.add_argument(
        "--file", help="Path to the file to be used to create the Customer, must be a JSON file", required=True
    )

    create_subscription_parser = subparsers.add_parser(
        "create_subscription", help="Create a subscription from a file with subscription items and a customer id"
    )
    create_subscription_parser.add_argument(
        "--file",
        help="Path to the file to be used to create the Subscription, must contain subscription items, must be a JSON file",
        required=True,
    )
    create_subscription_parser.add_argument("--customer_id", help="Valid Customer Id", required=True)

    create_customer_and_subscription_parser = subparsers.add_parser(
        "create", help="Create a customer and a subscription from two files"
    )
    create_customer_and_subscription_parser.add_argument(
        "--customer_file", help="Path to the file to the customer payload", required=True
    )
    create_customer_and_subscription_parser.add_argument(
        "--subscription_file", help="Path to the file of the subscription payload", required=True
    )

    args = parser.parse_args()

    command_map = {
        "get_customer_count": print_customer_count,
        "get_subscription_count": print_subscription_count,
        "get_customer_fields": print_customer_fields,
        "get_subscription_fields": print_subscription_fields,
        "get_customer_by_email": print_customer_by_email,
        "get_all_customers_emails": print_all_customers_emails,
        "get_customer_by_id": print_customer_by_id,
        "get_subscription_by_id": print_subscription_by_id,
        "get_all_subscription_ids": print_all_subscription_ids,
        "create_customer": create_customer_from_file,
        "create_subscription": create_subscription_from_file,
        "create": create_customer_and_subscription,
    }

    if args.command in command_map:
        command_map[args.command](args)
    else:
        print(f"Invalid command: {args.command}")


if __name__ == "__main__":
    main()
