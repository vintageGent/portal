# Professor's Lab Notes: Building the Recon Module (Step-by-Step)

In this lesson, we break down `recon.py` to see how a "Strategic Analyst" builds intelligence tools from scratch.

---

## Step 1: The Toolbox (Imports)
To build professional tools, we use three types of libraries:
1.  **Rich**: For the "Aesthetic." It creates the panels, tables, and colors that make your tool look like a Command Center.
2.  **Urllib**: This is the "Translator." It takes symbols like `@` or space and converts them into URL code (`%40`) so websites can read them.
3.  **OS & Webbrowser**: These are the "Connectors." They allow Python to command your computer to open folders or launch websites.

```python
from rich.console import Console # The screen
from rich.table import Table      # The report layout
import urllib.parse              # The URL translator
import webbrowser                # The browser launcher
```

---

## Step 2: The Logic (Domain Analysis)
We need to know *what* we are looking at. An email has two parts: `user` + `@` + `domain`.

```python
def analyze_domain(email):
    domain = email.split('@')[1] # Grab everything after the @
    
    # We maintain a list of 'Free' domains to spot common users vs targets
    personal_apps = ['gmail.com', 'yahoo.com', 'outlook.com']
    
    if domain in personal_apps:
        return domain, "Personal"
    else:
        return domain, "Corporate/Private"
```
**Strategic Why:** If the domain is `@cuk.ac.ke`, you know the target is an academic/corporate entity. This tells you that **LinkedIn** and **EPIEOS** are your strongest pivots.

---

## Step 3: The Engine (Pivot Generation)
This is the core of Recon. We take the target email and "inject" it into the search parameters of intelligence platforms.

```python
def generate_links(email):
    # We 'encode' the email so it works safely in a URL
    safe_email = urllib.parse.quote(email)
    
    # We build the exact search string for different sites:
    links = [
        {"name": "EPIEOS", "url": f"https://epieos.com/?q={safe_email}"},
        {"name": "LinkedIn", "url": f"https://www.linkedin.com/search/results/all/?keywords={safe_email}"}
    ]
    return links
```

---

## Step 4: The Interface (CLI Layout)
Finally, we display the findings in a `rich` Table. A professional tool shouldn't just print text; it should present a **Report**.

```python
table = Table(title="Intelligence Report")
table.add_column("Field", style="cyan")
table.add_column("Result", style="white")

table.add_row("Target", email)
table.add_row("Domain Status", domain_type)

console.print(table)
```

---

## Analyzing Your Target: `jgitari@cuk.ac.ke`
When you run the script with this email:
1.  **Analysis**: It flags it as "Corporate/Private (High Value)."
2.  **OSINT Links**:
    *   **LinkedIn**: Will bridge the gap to their professional title and potentially their phone number if listed.
    *   **EPIEOS**: Will check if they used this school email to sign up for things like Instagram or Facebook (often people reuse emails for convenience).
    *   **Google Dork**: Will find every PDF or Document on the `cuk.ac.ke` site that mentions this user.

**Lesson Summary:** You just built a tool that automates hours of manual searching into **two clicks**. 🛡️🔍
