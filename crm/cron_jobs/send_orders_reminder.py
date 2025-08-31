#!/usr/bin/env python3
import sys
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Log file
LOG_FILE = "/tmp/order_reminders_log.txt"

def main():
    # Calculate date range (last 7 days)
    today = datetime.utcnow()
    seven_days_ago = today - timedelta(days=7)

    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql(
        """
        query ($startDate: DateTime!) {
            orders(orderDate_Gte: $startDate, status: "PENDING") {
                id
                customer {
                    email
                }
                orderDate
            }
        }
        """
    )

    # Execute query
    params = {"startDate": seven_days_ago.isoformat()}
    try:
        result = client.execute(query, variable_values=params)
    except Exception as e:
        print(f"GraphQL query failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Setup logging
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )

    # Log each order
    for order in result.get("orders", []):
        logging.info("Order ID: %s, Customer Email: %s",
                     order["id"], order["customer"]["email"])

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
