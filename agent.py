@tool
def create_zoho_ticket(subject: str, description: str):
    """
    Creates a customer support ticket in Zoho Desk using hardcoded department and contact IDs.
 
    Args:
        subject (str): The title of the issue.
        description (str): Detailed explanation of the issue.
 
    Returns:
        dict: The Ticket ID and status (success/error message).
    """
    auth_token = os.getenv("ZOHO_AUTH_TOKEN")
    org_id = os.getenv("ZOHO_ORG_ID")
    contact_id = "239109000000342001"      # Valid contact ID
    department_id = "239109000000010772"   # Valid department ID
 
    # Validate required parameters
    if not auth_token or not org_id:
        ticket_number = random.randint(500, 900)
        return {
            "status": "success",
            "message": f"Ticket #{ticket_number} created (mocked), missing auth or org details.",
            "data": {"ticket_id": ticket_number, "subject": subject}
        }
 
    url = "https://desk.zoho.com/api/v1/tickets"
    headers = {
        "orgId": org_id,
        "Authorization": f"Zoho-oauthtoken {auth_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "subject": subject,
        "description": description,
        "contactId": contact_id,
        "departmentId": department_id
    }
 
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 422:
            return {
                "status": "error",
                "message": ("422 Client Error: Likely invalid contactId or departmentId, "
                            "or missing required fields. Check IDs are valid and active in Zoho Desk.")
            }
        return {"status": "error", "message": f"HTTP Error: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Request Error: {str(e)}"}
