import requests
import json

def test_cloudflare_credentials(credentials):
    url = f"https://api.cloudflare.com/client/v4/zones/{credentials['ZONE_ID']}"
    headers = {
        'X-Auth-Email': credentials['CLOUDFLARE_EMAIL'],
        'X-Auth-Key': credentials['CLOUDFLARE_API_KEY'],
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200

def main():
    credentials = {
        'CLOUDFLARE_API_KEY': input("Enter your Cloudflare Global API Key: "),
        'CLOUDFLARE_EMAIL': input("Enter your Cloudflare Email: "),
        'ZONE_ID': input("Enter your Cloudflare Zone ID: "),
        'USER_DOMAIN': input("Enter your domain (e.g., yourdomain.com): ")
    }

    if not test_cloudflare_credentials(credentials):
        print("Authentication with Cloudflare failed. Please check your credentials.")
        exit(1)

    proxy_choice = input("Proxied records or not proxied records?\n1- Not Proxied\n2- Proxied\nChoose (1/2): ")
    proxied = proxy_choice == '2'
    subdomain_choice = input("Do you want to use the default subdomain names or customize?\n1- Default\n2- Custom\nChoose (1/2): ")

    custom_subdomains = {}
    if subdomain_choice == '2':
        records = [
        "mcic.ircf.space", 
        "mtnc.ircf.space",
        "mkhc.ircf.space",
        "rtlc.ircf.space",
        "hwb.ircf.space",
        "ast.ircf.space",
        "sht.ircf.space",
        "prs.ircf.space",
        "mbt.ircf.space",
        "ask.ircf.space",
        "rsp.ircf.space",
        "afn.ircf.space",
        "ztl.ircf.space",
        "psm.ircf.space",
        "arx.ircf.space",
        "smt.ircf.space",
        "shm.ircf.space",
        "fnv.ircf.space",
        "dbn.ircf.space",
        "apt.ircf.space",
        "fnp.ircf.space",
        "ryn.ircf.space",
        "sbn.ircf.space",
        "ptk.ircf.space",
        "atc.ircf.space"
        ]
        for record in records:
            custom_subdomain = input(f"Enter new subdomain for '{record}': ")
            custom_subdomains[record] = custom_subdomain

    service_config = {
        'credentials': credentials,
        'proxied': proxied,
        'subdomain_choice': subdomain_choice,
        'custom_subdomains': custom_subdomains
    }

    with open('service.json', 'w') as file:
        json.dump(service_config, file)

    print("Service configuration saved.")

if __name__ == "__main__":
    main()
