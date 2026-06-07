#!/usr/bin/env python3
"""
Cyber Entidade — OSINT & Recon Automation
Coleta informações de domínio/empresa para pentest e bug bounty
"""
import subprocess, sys, json, os, datetime

TARGET = sys.argv[1] if len(sys.argv) > 1 else None
if not TARGET:
    print("Usage: osint.py <domain.com>")
    sys.exit(1)

TARGET = TARGET.replace('https://', '').replace('http://', '').split('/')[0]
OUTDIR = f"/home/roberto/projects/cyber-entidade/osint/{TARGET.replace('.','_')}_{datetime.date.today()}"
os.makedirs(OUTDIR, exist_ok=True)

def run(cmd, fname, timeout=120):
    path = f"{OUTDIR}/{fname}"
    print(f"[*] {fname}...")
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        with open(path, 'w') as f:
            f.write(r.stdout)
        return r.stdout.strip()
    except Exception as e:
        return str(e)

print(f"Cyber Entidade OSINT v1.0 — {TARGET}\n")

results = {}

# 1. WHOIS
results['whois'] = run(f"whois {TARGET}", "01_whois.txt", timeout=30)

# 2. DNS records
results['dig'] = run(f"dig {TARGET} ANY +noall +answer", "02_dns.txt")

# 3. Subdomain enum (if subfinder available)
results['subdomains'] = run(f"subfinder -d {TARGET} -silent 2>/dev/null || echo 'subfinder not installed'", "03_subdomains.txt")

# 4. Shodan (if CLI available)
results['shodan'] = run(f"shodan domain {TARGET} 2>/dev/null || echo 'shodan not installed'", "04_shodan.txt")

# 5. Wayback URLs
results['wayback'] = run(f"curl -s 'https://web.archive.org/cdx/search/cdx?url=*.{TARGET}&output=text&fl=original&collapse=urlkey' 2>/dev/null | head -100", "05_wayback.txt", timeout=30)

# 6. Certificate transparency
results['crt'] = run(f"curl -s 'https://crt.sh/?q=%25.{TARGET}&output=json' 2>/dev/null | python3 -c \"import json,sys; data=json.load(sys.stdin); [print(d['name_value']) for d in data]\" 2>/dev/null | sort -u | head -50", "06_crtsh.txt", timeout=30)

# Generate report
report = f"""# OSINT Report — {TARGET}
**Date:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}

## Quick Summary
- **WHOIS:** {'Available' if 'No match' in results.get('whois','') else 'Registered'}
- **Subdomains found:** {len(results.get('subdomains','').split(chr(10))) if results.get('subdomains') else 0}
- **Wayback URLs:** {len(results.get('wayback','').split(chr(10))) if results.get('wayback') else 0}

## Files
| File | Content |
|------|---------|
| `01_whois.txt` | Domain registration info |
| `02_dns.txt` | DNS records |
| `03_subdomains.txt` | Subdomain enumeration |
| `04_shodan.txt` | Shodan data |
| `05_wayback.txt` | Historical URLs |
| `06_crtsh.txt` | Certificate Transparency logs |

---
*Cyber Entidade — Automated OSINT*
"""

with open(f"{OUTDIR}/REPORT.md", 'w') as f:
    f.write(report)

print(f"\n✅ OSINT complete! Report: {OUTDIR}/REPORT.md")
