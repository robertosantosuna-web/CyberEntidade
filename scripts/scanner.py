#!/usr/bin/env python3
"""
Cyber Entidade — Scanner de Segurança Automatizado
Scan rápido usando Nmap + Nikto + relatório Markdown
"""
import subprocess, sys, json, os, datetime

TARGET = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
OUTDIR = f"/home/roberto/projects/cyber-entidade/scans/{TARGET.replace('.','_')}_{datetime.date.today()}"
os.makedirs(OUTDIR, exist_ok=True)

def run(cmd, fname):
    """Run command, save output"""
    path = f"{OUTDIR}/{fname}"
    print(f"[*] Running: {cmd[:80]}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        with open(path, 'w') as f:
            f.write(result.stdout)
        return result.stdout
    except Exception as e:
        return f"ERROR: {e}"

print(f"""
╔══════════════════════════════════╗
║   Cyber Entidade Scanner v1.0   ║
║   Target: {TARGET:<21}║
╚══════════════════════════════════╝
""")

# 1. Nmap rápido portas comuns
nmap_quick = run(f"nmap -T4 -F {TARGET}", "01_nmap_quick.txt")

# 2. Nmap completo com scripts de vuln
nmap_full = run(f"nmap -T4 -sV -sC --script=vuln {TARGET}", "02_nmap_full.txt")

# 3. Nikto scan
nikto = run(f"nikto -h {TARGET} -T 2", "03_nikto.txt") if os.system("which nikto >/dev/null 2>&1") == 0 else "Nikto not installed"

# 4. WhatWeb
whatweb = run(f"whatweb {TARGET}", "04_whatweb.txt") if os.system("which whatweb >/dev/null 2>&1") == 0 else "WhatWeb not installed"

# Generate report
report = f"""# Scan Report — {TARGET}
**Date:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
**Company:** Cyber Entidade

## Summary
- **Target:** {TARGET}
- **Scan type:** Quick + Full + Vuln

## Results
See detailed output files in `{OUTDIR}/`

### Open Ports Summary
```
{chr(10).join([l for l in nmap_quick.split(chr(10)) if 'open' in l.lower() or 'PORT' in l])[:500]}
```

## Files
- `01_nmap_quick.txt` — Quick scan (top 100 ports)
- `02_nmap_full.txt` — Full scan with version detection + vuln scripts
- `03_nikto.txt` — Web server scan
- `04_whatweb.txt` — Technology detection

---
*Cyber Entidade — Automated Security Scan*
"""

with open(f"{OUTDIR}/REPORT.md", 'w') as f:
    f.write(report)

print(f"\n✅ Scan complete! Report: {OUTDIR}/REPORT.md")
print(f"   Files saved to: {OUTDIR}/")
