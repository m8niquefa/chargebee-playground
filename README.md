# chargebee-playground
Just a simple Repo to play around with the chargebee API

# Secrets
Be sure to have in your secrets and/or environmental variables:

```
CHARGE_BEE_API_KEY=
CHARGE_BEE_URL=
```


# Commands available

## Get help and commands available

* ```python3 cli.py -h```

### Output
```
[OK] Load environment variables
[OK] Configured chargebee
usage: cli.py [-h]
              {get_customer_count,get_subscription_count,get_customer_fields,get_subscription_fields,get_customer_by_email,get_all_customers_emails,get_customer_by_id,get_subscription_by_id,get_all_subscription_ids,create_customer,create_subscription}
              ...

MachEight Chargebee CLI playground

positional arguments:
  {get_customer_count,get_subscription_count,get_customer_fields,get_subscription_fields,get_customer_by_email,get_all_customers_emails,get_customer_by_id,get_subscription_by_id,get_all_subscription_ids,create_customer,create_subscription}
    get_customer_count  Get customer count
    get_subscription_count
                        Get Subscription count
    get_customer_fields
                        Get customer fields
    get_subscription_fields
                        Get Subscription fields
    get_customer_by_email
                        Get customer by email
    get_all_customers_emails
                        Get all customers emails
    get_customer_by_id  Get customer by id
    get_subscription_by_id
                        Get Subscription by id
    get_all_subscription_ids
                        Get all subscription ids
    create_customer     Create a customer from a file
    create_subscription
                        Create a subscription from a file with subscription items and a customer id

options:
  -h, --help            show this help message and exit
```

# Example of usage

```python cli.py get_customer_count```

## Example of output

```
[OK] Load environment variables
[OK] Configured chargebee
Customer count: 47
```

# Examples of commands

* ```python cli.py get_customer_by_id --id SOME_VALID_STRING_ID```
* ```python cli.py get_customer_by_email --email SOME_EMAIL@SOMEDOMAIN.COM```
* ```python cli.py create_customer --file customer_example.json```
* ```python cli.py create_subscription --customer_id SOME_VALID_STRING_ID --file items_for_subscription_example.json```
* ```python cli.py get_subscription_by_id --id SOME_VALID_STRING_ID```