# Plataformas de Bug Bounty

## Plataformas Ativas

| Plataforma | URL | Foco | Mínimo Recompensa |
|-----------|-----|------|-------------------|
| **HackerOne** | hackerone.com | Geral (Google, GitHub, etc) | $150-30,000+ |
| **Bugcrowd** | bugcrowd.com | Enterprise | $100-10,000+ |
| **Intigriti** | intigriti.com | Europa | €50-15,000+ |
| **YesWeHack** | yeswehack.com | França/Global | €50-5,000+ |
| **Synack** | synack.com | Red Team (convidado) | $500-20,000+ |
| **Open Bug Bounty** | openbugbounty.org | Coordinated disclosure | Variável |

## Programas Recomendados (Iniciante)

### HackerOne
1. **Internet Bug Bounty** — vulnerabilidades em padrões web (CORS, CSP, etc)
2. **Shopify** — boa documentação, escopo claro
3. **GitLab** — programas públicos bem definidos
4. **U.S. Dept of Defense** — Hack the Pentagon

### Bugcrowd
1. **Tesla** — recompensas altas, escopo específico
2. **Atlassian** — Jira, Confluence, etc
3. **OpenSSL** — crítico para internet

### Intigriti
1. **European Commission** — programas públicos
2. **Showpad** — SaaS belga
3. **Intigriti CTF** — desafios próprios com recompensa

## Metodologia de Caça

### 1. Reconhecimento
```bash
# Subdomain enum
subfinder -d target.com
assetfinder target.com

# Port scan
nmap -T4 -p- target.com

# Tech stack
whatweb target.com
wappalyzer target.com
```

### 2. Enumeração
```bash
# Directory bruteforce
ffuf -w /usr/share/wordlists/dirb/common.txt -u https://target.com/FUZZ

# Parameter discovery
arjun -u https://target.com/page

# JavaScript analysis
python3 linkfinder.py -i script.js -o links.txt
```

### 3. Exploração
- XSS: `<script>alert(document.domain)</script>`
- SQLi: `' OR '1'='1' --`
- IDOR: Insecure Direct Object Reference
- CSRF: Cross-Site Request Forgery
- SSRF: Server-Side Request Forgery

## Ferramentas

| Ferramenta | Uso |
|-----------|-----|
| Burp Suite Community | Proxy + scanner manual |
| ffuf | Fuzzing |
| nuclei | Template-based scanning |
| sqlmap | SQL Injection |
| amass | OSINT / DNS enum |
| subfinder | Subdomain discovery |
| httpx | HTTP probing |
| katana | Crawling |

## Setup Rápido

```bash
# Instalar ferramentas básicas
sudo apt install -y nmap nikto whatweb

# Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/ffuf/ffuf/v2@latest

# Python
pip install arjun sqlmap
```
