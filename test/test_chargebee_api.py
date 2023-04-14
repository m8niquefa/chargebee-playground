import json
import pprint
import unittest
import chargebee

from chargebee.api_error import APIError

from unittest.mock import MagicMock, patch

from cp import create_chargebee_customer_with_subscription

class TestCreateChargebeeCustomerWithSubscription(unittest.TestCase):
    def setUp(self):
        self.data_for_customer_creation = {"email": "johndoe14@test.com"}
        self.subscription_data = {
            "subscription_items": [
                {
                    "item_price_id": "drm",
                    "item_type": "plan",
                    "object": "subscription_item",
                    "quantity": 1,
                }
            ],
            "auto_collection": "off",
        }

    @patch("chargebee.Customer.create")
    @patch("chargebee.Subscription.create_with_items")
    def test_create_chargebee_customer_with_subscription_success(self, mock_create_subscription, mock_create_customer):
        mock_customer = MagicMock()
        mock_customer.id = "test_customer_id"
        mock_subscription = MagicMock()

        mock_create_customer.return_value = mock_customer
        mock_create_subscription.return_value = mock_subscription

        created_customer, created_subscription = create_chargebee_customer_with_subscription(
            self.data_for_customer_creation, self.subscription_data
        )

        self.assertEqual(created_customer, mock_customer)
        self.assertEqual(created_subscription, mock_subscription)

        mock_create_customer.assert_called_once_with(self.data_for_customer_creation)
        mock_create_subscription.assert_called_once_with(mock_customer.id, self.subscription_data)

    @patch("chargebee.Customer.create")
    def test_create_chargebee_customer_returns_none(self, mock_create_customer):
        mock_create_customer.return_value = None

        created_customer, created_subscription = customer.create_chargebee_customer_with_subscription(
            self.data_for_customer_creation, self.subscription_data
        )

        self.assertIsNone(created_customer)
        self.assertIsNone(created_subscription)

    @patch("chargebee.Customer.create")
    @patch("chargebee.Subscription.create_with_items")
    def test_create_chargebee_subscription_returns_none(self, mock_create_subscription, mock_create_customer):
        mock_customer = MagicMock()
        mock_customer.id = "test_customer_id"

        mock_create_customer.return_value = mock_customer
        mock_create_subscription.side_effect = APIError(
            http_code=400,
            json_obj={
                "message": "Customer and Subscription creation failed",
                "type": "request error",
                "api_error_code": "resource_not_found",
                "param": "customer_id",
                "error_code": "error_code_for_test"
            }
        )

        created_customer, created_subscription = create_chargebee_customer_with_subscription(
            self.data_for_customer_creation, self.subscription_data
        )

        self.assertIsNotNone(created_customer)
        self.assertIsNone(created_subscription)

    # def test_create_chargebee_customer_with_subscription_success(self):
    #     created_customer, created_subscription = create_chargebee_customer_with_subscription(
    #         self.data_for_customer_creation, self.subscription_data
    #     )

if __name__ == "__main__":
    unittest.main()