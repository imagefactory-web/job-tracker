import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# Google Sheets auth
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)
client = gspread.authorize(creds)
sheet = client.open("Global_DevOps_Relocation_Jobs").sheet1

# Fetch jobs from RemoteOK
url = "https://remoteok.com/api"
jobs = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()[1:]

for job in jobs:
    title = job.get("position", "").lower()

    if any(k in title for k in ["devops", "sre", "cloud"]):
        description = job.get("description", "").lower()

        relocation = "Yes" if any(
            k in description for k in
            ["relocation", "visa", "sponsorship", "work permit"]
        ) else "Unknown"

        sheet.append_row([
            job.get("company"),
            job.get("position"),
            "DevOps/SRE",
            "Global",
            job.get("location", "Remote"),
            "Yes",
            relocation,
            "Unknown",
            "AWS, Terraform, Kubernetes",
            "RemoteOK",
            job.get("url"),
            str(date.today())
        ])
