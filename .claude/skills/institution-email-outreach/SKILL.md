---
name: institution-email-outreach
description: Personal email outreach campaigns from Liraz Tal (מרכז טל) to institutions — שפ״חים, בתי ספר, יועצות, מנהלי בתי ספר, מתי״אות, מרפאות, רשויות, עמותות, אקדמיה — offering lectures, trainings or groups. Covers finding and verifying recipient addresses (including Gemini prompts), building a Hebrew RTL "landing page" email, sending one personal message per institution from the connected Gmail, duplicate and bounce checks, a tracking sheet, and warm replies to positive responses. Use this whenever Liraz wants to reach out by email to a list of organizations, find contact emails for institutions, prepare a Gemini/ChatGPT prompt for finding contacts, check who answered or bounced, or reply to responses — even if she only says "לשלוח לכל ה..." or "תכין פרומפט לגמיני".
---

# Institution email outreach (מרכז טל)

This skill captures a workflow that was refined over a real campaign (≈80 institutions, October 2026). Most rules below exist because something went wrong without them — the reason is given so you can apply the spirit, not just the letter.

## 0. Before anything: settle the brief

Confirm with Liraz (briefly, only what's missing):
- **What is offered** (e.g. הרצאה/השתלמות "הסמכות ההורית המארגנת", or קבוצות חברתיות לתלמידים) and the key content.
- **Who** (type of institution, role: מנהל/ת, יועצת, רכזת) and **where** (radius from צפריה, e.g. 25 ק״מ).
- **Sender**: the connected Gmail (liraztalpsy@gmail.com). Phone in emails: **058-788-7433** (the center's number, connected to a bot).
- Whether there's a source list (Excel/CSV she uploads) — always use it first.

Standing preferences (keep unless she changes them):
- Greeting with **first name only** ("שלום דגנית,"). If no confirmed name → "שלום לצוות ה...". Never guess a name from an email address.
- When naming the method: **"הסמכות ההורית המארגנת" always before "מודל PORA"**.
- **No automatic follow-up emails.** Each sending round needs her explicit approval.
- Report "נשלח" only after Gmail returns a message id.
- Replies to responses: signature **"לירז"** only; price is discussed **only after a short call**.

## 1. Find addresses

Order of sources: her file → official sites (רשות, משרד החינוך, קופות, בתי חולים) → Gemini/ChatGPT with a strict prompt (see `references/gemini_prompt.md`).

Verification standard (why: Gemini repeatedly invented addresses by pattern, e.g. `holon@amcha.org` instead of `Amcha_Holon@amcha.org`, and wrong domains like `ramla.muni.il` vs the real `ramle.org.il`):
- An address is **verified** only if it appears verbatim on a live page/document. Check with `WebSearch` (mode `extended`, quote the address, or `allowed_domains` of the institution). Many municipal sites are blocked for `WebFetch` by the egress proxy — search results are the practical way to confirm.
- Do not build addresses from patterns, and don't use contact forms or 106 hotlines as a substitute.
- One recipient per institution. Prefer the head's direct address; else the service's own address (not the city's general inbox).
- **Current rule (from 2026-10-08): send only to verified addresses.** Earlier in the campaign Liraz allowed unverified ones ("מקסימום יחזור"); after several bounces and a Gemini batch with fabricated addresses and recycled סמל מוסד numbers, she reversed it: "לא לשלוח למה שלא מאומת ויכול לחזור". Unverified candidates go to the phone list instead. An address shown on an official page but hidden by email obfuscation (Cloudflare "[email protected]") counts as unverified unless she approves it explicitly.
- Red flags that a Gemini batch is invented: the same סמל מוסד numbers reused for different schools across batches, a source site that doesn't exist (e.g. "shkifut.education.gov.il/institution/..."), quotes that are only "דואר אלקטרוני: x@gmail.com", more schools than the municipality says exist. Ministry of Education lists (meyda.education.gov.il PDFs) are official but sometimes contain typos (`Shapacj@` → `Shapach@`, `munu.il`).

Present each candidate batch as a table: גוף | נמען | פתיחה | איך אומת/הערה, plus what you recommend skipping and why. Wait for approval.

## 2. Duplicate check (always, right before sending)

`search_threads` with `in:sent (to:a OR to:b ...)`. Also think at the **organization** level: a second address of an institution that already got the offer is a duplicate (e.g. general `sph@` after the manager's direct address was sent). Skip those and say so.

## 3. Build the email

Use `scripts/build_email.py` with a content file (see `assets/example_content.json` — the PORA campaign) and a recipients file. It produces, per recipient, a JSON with `to`, `subject`, `body` (plain text) and `htmlBody`.

Design rules learned the hard way:
- **No colored-background buttons.** In Gmail mobile, `<a>` with background renders as an empty frame and white text disappears. Use plain underlined purple links.
- **No heavy attachments.** The Gmail tool sends attachments inline as base64; a 186KB PDF was impractical. Put files on Drive (shared "anyone with the link") and link them. Keep an inline "landing page" card in the email instead.
- RTL: wrap everything in `<div dir="rtl" style="direction:rtl;text-align:right">`. Always include a plain-text `body` too.
- Adapt **one offer sentence + subject + card kicker** per institution type (שפ״ח / מתי״א / מרכז הורים / אקדמיה / בית ספר) — the rest of the text stays identical. Keep the original wording she approved; don't rewrite her story paragraphs.

Show her one rendered sample (or the text) before the first round of a new campaign.

Marketing copy (new offers, webinar invitations, course announcements) follows her standing guidelines in `.claude/skills/marketing-content/SKILL.md`: identification → understanding → hope → one call to action, and never teach the "how" of the method in promotional text.

## 4. Send

`send_message` once per recipient (`to`, `subject`, `body`, `htmlBody`). Send in batches of ~4–5 calls per turn. For corrections to an existing message, use `replyThreadId` of the original thread so it stays in one conversation.

## 5. After sending

- Check bounces: `from:mailer-daemon newer_than:1h`. `550 5.4.1 Recipient address rejected` = the address doesn't exist. Some servers bounce hours later — check again next day.
- Classify incoming: real reply / auto-reply (e.g. "פנייתך התקבלה", "מענה אוטומטי") / bounce. Auto-replies from health providers are parent-intake acknowledgements — the message arrived, nothing more.
- Update the tracking file (`references/tracking.md` for columns). There is usually no Google Sheets editor connector: give her tab-separated rows to paste, and explain that turning on Google Sheets in a **new** session would let you write directly.
- Offer a scheduled check (e.g. next morning 09:00 Israel) via `send_later`; the check only reports and drafts — never sends.

## 6. Replies to positive responses

Use `references/reply_templates.md` (interested / forwarding / price question). Personalize to what they wrote; signature "לירז"; propose a 15–20 minute call and a written proposal afterwards. For a personal acquaintance (e.g. a former supervisor) write short, warm, without a sales pitch — ask her what's true about the relationship rather than inventing shared memories. Always show the draft and get approval before sending.

## Next campaign note — schools / קבוצות חברתיות

For יועצות ומנהלי בתי ספר: school emails are often on municipal education pages, school sites (tik-tak, edu.gov.il school pages, `school-name@...`), or the Ministry's school directory by סמל מוסד. Counselors' personal emails are rarely public — the school's office address with "לכבוד היועצת" in the greeting is an acceptable fallback if Liraz agrees. Adapt the content file (what the groups are, age range, format, funding routes such as גפ״ן — she is registered in גפ״ן) before building.

The approved text for this campaign (from 2026-10-08) is in `references/groups_email_template.md`: identification-first opening, no "how" details, landing page then WhatsApp channel at the end.
