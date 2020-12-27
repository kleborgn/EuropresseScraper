import requests
import re
import urllib.parse
import json
import rm_dupes
import makepdf
import datetime
import send_mail

url = 'https://nouveau.europresse.com/access/ip/default.aspx?un=BDP'
url2 = 'https://nouveau.europresse.com/Pdf/Edition?sourceCode=LM_P'

# Get login cookie
s = requests.Session()
r = s.get(url)

# Get pdf reader page
r2 = s.get(url2)

p = re.compile('(?<=_docNameList = )(.*)(?=;)')

parsed = p.findall(r2.text)

pages = json.loads(parsed[0])

pageNb = 1

print("[+] Downloading pages...")

for page in pages:
    eurl = urllib.parse.quote(page, safe='~()*!.\'')
    r3 = s.get("https://nouveau.europresse.com/Pdf/ImageList?docName=" + eurl)

    r4 = s.get("https://nouveau.europresse.com/Pdf/Image?imageIndex=0&id=" + eurl)

    file = open(str(pageNb) + ".png", "wb")
    file.write(r4.content)
    file.close()
    pageNb+=1

# Delete dupes

print("[+] Checking for duplicates...")
rm_dupes.check_for_duplicates('.')
print("[+] Duplicates deleted.")
# Make PDF

print("[+] Making PDF...")
makepdf.makePdf("LeMonde", '.')

# Send email
print("[+] Sending mail...")
send_mail.send()
print("[+] Mail sent !")
# Clear

print("Clearing files...")
rm_dupes.clear('.')
