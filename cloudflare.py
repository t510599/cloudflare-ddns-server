import requests as r


class CloudflareAPI:
    endpoint = "https://api.cloudflare.com/client/v4"

    def __init__(self, token, zone_id):
        self.zone_id = zone_id
        self.session = r.Session()
        self.session.headers = {
            "Authorization": f"Bearer {token}"
        }

    def zone_result(self, domain):
        if not domain:
            return None

        res = self.session.get(f"{self.endpoint}/zones/{self.zone_id}/dns_records?name={domain}")
        data = res.json()

        return data["result"][0].get("id") if data["result_info"]["count"] > 0 else ""

    def update_result(self, domain, ip, record_type="A", ttl=1):
        if not domain:
            return None

        cf_id = self.zone_result(domain)

        if not cf_id:
            return None

        res = self.session.put(
                f"{self.endpoint}/zones/{self.zone_id}/dns_records/{cf_id}",
                json={
                    "type": record_type,
                    "name": domain,
                    "content": ip,
                    "ttl": str(ttl)
                }
              )
        data = res.json()

        return data["success"]