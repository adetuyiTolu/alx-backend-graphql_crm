import datetime
import requests
from celery import shared_task

@shared_task
def generate_crm_report():
    """
    Generates a weekly CRM report using requests to call GraphQL and logs it.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = "/tmp/crm_report_log.txt"

    url = "http://localhost:8000/graphql"
    query = """
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
    """

    try:
        response = requests.post(url, json={"query": query})
        response.raise_for_status()
        data = response.json()["data"]

        total_customers = data["allCustomers"]["totalCount"]
        total_orders = data["allOrders"]["totalCount"]
        total_revenue = sum(edge["node"]["totalAmount"] for edge in data["allOrders"]["edges"])

        report_line = f"{now} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

        with open(log_file_path, "a") as f:
            f.write(report_line)

    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{now} - ERROR generating report: {str(e)}\n")
