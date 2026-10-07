import unittest

from framework.data_quality import (
    validate_required_columns,
    find_null_records,
    find_duplicate_records
)


class TestDataQuality(unittest.TestCase):

    def setUp(self):
        self.records = [
            {
                "customer_id": "C1001",
                "customer_name": "John Carter",
                "email": "john@example.com"
            },
            {
                "customer_id": "C1002",
                "customer_name": "Sarah Miller",
                "email": "sarah@example.com"
            }
        ]

    def test_required_columns(self):
        missing_columns = validate_required_columns(
            self.records,
            [
                "customer_id",
                "customer_name",
                "email"
            ]
        )

        self.assertEqual(
            missing_columns,
            []
        )

    def test_null_detection(self):
        records = [
            {
                "customer_id": "C1001",
                "customer_name": ""
            }
        ]

        invalid_records = find_null_records(
            records,
            [
                "customer_id",
                "customer_name"
            ]
        )

        self.assertEqual(
            len(invalid_records),
            1
        )

    def test_duplicate_detection(self):
        records = [
            {"customer_id": "C1001"},
            {"customer_id": "C1001"}
        ]

        duplicates = find_duplicate_records(
            records,
            ["customer_id"]
        )

        self.assertEqual(
            len(duplicates),
            2
        )


if __name__ == "__main__":
    unittest.main()
