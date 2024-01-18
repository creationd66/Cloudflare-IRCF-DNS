import requests
import socket
from urllib.parse import urlparse
import json
import os

config_file = 'config.json'
def test_cloudflare_credentials(credentials):
    url = f"https://api.cloudflare.com/client/v4/zones/{credentials['ZONE_ID']}"
    headers = {
        'X-Auth-Email': credentials['CLOUDFLARE_EMAIL'],
        'X-Auth-Key': credentials['CLOUDFLARE_API_KEY'],
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200

def load_or_request_credentials():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)
    else:
        credentials = {
            'CLOUDFLARE_API_KEY': input("Enter your Cloudflare Global API Key: "),
            'CLOUDFLARE_EMAIL': input("Enter your Cloudflare Email: "),
            'ZONE_ID': input("Enter your Cloudflare Zone ID: "),
            'USER_DOMAIN': input("Enter your domain (e.g., yourdomain.com): ")
        }

        if test_cloudflare_credentials(credentials):
            with open(config_file, 'w') as file:
                json.dump(credentials, file)
            return credentials
        else:
            print("Authentication with Cloudflare failed. Please check your credentials.")
            exit(1)

# Rest of the script remains the same


records = [
    ("mcic.ircf.space", "همراه اول"),
    ("mtnc.ircf.space", "ایرانسل"),
    ("mkhc.ircf.space", "مخابرات"),
    ("rtlc.ircf.space", "رایتل"),
    ("hwb.ircf.space", "های وب"),
    ("ast.ircf.space", "آسیاتک"),
    ("sht.ircf.space", "شاتل"),
    ("prs.ircf.space", "پارس آنلاین"),
    ("mbt.ircf.space", "مبین نت"),
    ("ask.ircf.space", "اندیشه سبز"),
    ("rsp.ircf.space", "رسپینا"),
    ("afn.ircf.space", "افرانت"),
    ("ztl.ircf.space", "زی تل"),
    ("psm.ircf.space", "پیشگامان"),
    ("arx.ircf.space", "آراکس"),
    ("smt.ircf.space", "سامان تل"),
    ("shm.ircf.space", "شاتل موبایل"),
    ("fnv.ircf.space", "فن آوا"),
    ("dbn.ircf.space", "دیده بان نت"),
    ("apt.ircf.space", "آپتل"),
    ("fnp.ircf.space", "فناپ تلکام"),
    ("ryn.ircf.space", "رای نت"),
    ("sbn.ircf.space", "صبانت"),
    ("ptk.ircf.space", "پتیاک"),
    ("atc.ircf.space", "عصر تلکام"),
]


def get_external_ip(url):
    try:
        if '://' not in url:
            url = 'http://' + url
        hostname = urlparse(url).hostname
        return socket.gethostbyname(hostname)
    except Exception as e:
        print(f"Error getting IP: {e}")
        return None


def get_dns_record_id(subdomain, credentials):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{credentials['ZONE_ID']}/dns_records?type=A&name={subdomain}"
        headers = {
            'X-Auth-Email': credentials['CLOUDFLARE_EMAIL'],
            'X-Auth-Key': credentials['CLOUDFLARE_API_KEY'],
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.json()['result']:
            return response.json()['result'][0]['id']
    except Exception as e:
        print(f"Error getting DNS record ID: {e}")
    return None

def delete_dns_record(record_id, credentials):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{credentials['ZONE_ID']}/dns_records/{record_id}"
        headers = {
            'X-Auth-Email': credentials['CLOUDFLARE_EMAIL'],
            'X-Auth-Key': credentials['CLOUDFLARE_API_KEY'],
            'Content-Type': 'application/json'
        }
        response = requests.delete(url, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"Error deleting DNS record: {e}")
        return False

def create_dns_record(ip, comment, subdomain, proxied, credentials):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{credentials['ZONE_ID']}/dns_records"
        headers = {
            'X-Auth-Email': credentials['CLOUDFLARE_EMAIL'],
            'X-Auth-Key': credentials['CLOUDFLARE_API_KEY'],
            'Content-Type': 'application/json'
        }
        data = {
            'type': 'A',
            'name': subdomain,
            'content': ip,
            'ttl': 1,
            'comment': comment,
            'proxied': proxied
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to create DNS record. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error creating DNS record: {e}")
        return False

def main():
    credentials = load_or_request_credentials()

    proxy_choice = input("Proxied records or not proxied records?\n1- Not Proxied\n2- Proxied\nChoose (1/2): ")
    proxied = proxy_choice == '2'

    subdomain_choice = input("Do you want to use the default subdomain names or customize?\n1- Default\n2- Custom\nChoose (1/2): ")

    updated_records = []
    for original_domain, comment in records:
        ip = get_external_ip(original_domain)
        if ip:
            if subdomain_choice == '2':
                new_subdomain = input(f"Enter new subdomain for '{original_domain}' (Comment: {comment}): ") + '.' + credentials['USER_DOMAIN']
            else:
                new_subdomain = original_domain.split('.')[0] + '.' + credentials['USER_DOMAIN']
            updated_records.append((new_subdomain, ip, comment))

    for new_subdomain, ip, comment in updated_records:
        record_id = get_dns_record_id(new_subdomain, credentials)
        if record_id:
            delete_dns_record(record_id, credentials)
        if create_dns_record(ip, comment, new_subdomain, proxied, credentials):
            print(f"DNS record for {new_subdomain} ({comment}) created successfully")
        else:
            print(f"Failed to create DNS record for {new_subdomain}")

if __name__ == "__main__":
    main()
