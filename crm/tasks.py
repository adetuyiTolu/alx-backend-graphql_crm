import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """
    Generates a weekly CRM report and logs it.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = "/tmp/crm_report_log.txt"

    # Configure GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql("""
        query {
            allCustomers {
                totalCount
            }
            allOrders {
                totalCount
                edges {
                    node {
                        totalAmount
                    }
                }
            }
        }
    """)

    try:
        result = client.execute(query)
        total_customers = result["allCustomers"]["totalCount"]
        total_orders = result["allOrders"]["totalCount"]
        total_revenue = sum([edge["node"]["totalAmount"] for edge in result["allOrders"]["edges"]])

        report_line = f"{now} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
        with open(log_file_path, "a") as f:
            f.write(report_line)

    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{now} - ERROR generating report: {str(e)}\n")
