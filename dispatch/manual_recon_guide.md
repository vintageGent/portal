# The Seeker's OSINT Handbook: Manual Reverse Email Lookups

Building a script is great, but a true **Cyber-PR Strategist** knows how to hunt manually when the tools hit a wall. Here is the step-by-step breakdown of how I found Dr. James Gitari.

---

## Step 1: The "Google Dork" (Precision Searching)
Regular Googling is too noisy. We use "Dorks" to force Google to show us exact matches.

**What I did:**
I searched for: `intext:"jgitari@cuk.ac.ke"`

*   **Logic**: The `intext:` operator tells Google: "Only show me pages where this exact string of text appears *inside* the page content."
*   **Result**: This bypassed thousands of "CUK" results and took me directly to a PDF listing the **CUK Faculty of Commerce Staff List**.

---

## Step 2: The "Identity Pivot" (Name Hunting)
Once the "Dork" gave me the name **James Gitari**, the email was no longer just a string—it was a person.

**The Pivot:**
Knowing he is at **CUK**, I searched: `site:cuk.ac.ke "James Gitari"`

*   **Logic**: the `site:` operator limits results to a specific domain.
*   **Result**: I found his research profile, which confirmed he has a **PhD** and is a specialist in **MIS (Management Information Systems)**.

---

## Step 3: Social & Academic Recon
Professional targets (Lecturers, CEOs, Gov Officials) usually don't hang out on Instagram. They live on **LinkedIn** and **ResearchGate**.

**The Tactic:**
1.  **LinkedIn**: Search for the full name + Organization.
2.  **ResearchGate/Google Scholar**: Search for the name. Academic papers often have a "Contact" or "Corresponding Author" section at the bottom of the first page.

---

## Step 4: Finding the "Warm" Contact (Phone/Desk)
If the direct email fails, you look for the **Proximity Contact**.

**What I did:**
I searched for the **CUK Faculty of Commerce Office Number**. 
*   **Logic**: It is much harder for a professor to ignore a "Transfer" from their own department secretary than a random external email.
*   **Finding**: The university lists `0724 311 606` as a direct line for inquiries.

---

## 🛠️ Your Exercise: Run a Manual Hunt
Try this on another email (maybe your own or a public figure's):

1.  **Dork the Email**: `intext:"target@email.com"`
2.  **Dork the Domain**: `site:domain.com "Lastname"`
3.  **Check the Breach**: Go to [HaveIBeenPwned](https://haveibeenpwned.com) and see *when* they were leaked. (If they haven't been leaked since 2018, they might have changed their passwords/emails).

**The Secret:** Recon isn't about one "big find"—it's about connecting small dots until they form a picture. 🛡️🔍
