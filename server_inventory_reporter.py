def validate_server(server):
    """
    Validate a single server dictionary.

    Rules:
    - server must be a dict
    - must contain keys 'name', 'region', 'status'
    - 'name' must be a non-empty string
    - 'region' must be a non-empty string
    - 'status' must be either 'active' or 'inactive' (exact match)
    """
    if not isinstance(server, dict):
        return False

    required = {"name", "region", "status"}
    if not required.issubset(server.keys()):
        return False

    name = server.get("name")
    region = server.get("region")
    status = server.get("status")

    if not isinstance(name, str) or name.strip() == "":
        return False

    if not isinstance(region, str) or region.strip() == "":
        return False

    if status not in ("active", "inactive"):
        return False

    return True


def generate_inventory_report(servers):
    """
    Generate inventory report from a list of server dicts.

    - Uses validate_server to skip invalid entries.
    - Returns a dict keyed by region, each value is a dict:
        {'active': [...], 'inactive': [...]}
    - Keeps server name order as in input.
    """
    report = {}

    for srv in servers:
        if not validate_server(srv):
            continue

        region = srv["region"]
        name = srv["name"]
        status = srv["status"]  # 'active' or 'inactive'

        if region not in report:
            report[region] = {"active": [], "inactive": []}

        report[region][status].append(name)

    return report

servers = [
    {"name": "web-01", "region": "us-east-1", "status": "active"},
    {"name": "db-01",  "region": "us-east-1", "status": "inactive"},
    {"name": "cache",  "region": "eu-west-1", "status": "active"},
    {"name": "",       "region": "eu-west-1", "status": "active"},         # invalid: empty name
    {"name": "api-01", "region": "us-east-1", "status": "unknown"},        # invalid: bad status
    {"name": "worker", "region": "us-east-1", "status": "active"},
]

print(validate_server(servers[0]))  # True
print(validate_server(3))           # False (not a dict)
print(validate_server(servers[3]))  # False (empty name)

report = generate_inventory_report(servers)
print(report)