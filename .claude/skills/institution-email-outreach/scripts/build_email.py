"""Build personal Hebrew RTL outreach emails (plain text + Gmail-safe HTML).

Usage:
  python build_email.py content.json recipients.json out_dir

recipients.json: list of objects
  {"email": "...", "greeting_name": "דגנית" | null, "team_label": "לצוות השפ״ח", "kind": "shapach"}
  - greeting_name set   -> "שלום דגנית,"
  - otherwise           -> "שלום <team_label>,"
  - kind selects the offer sentence / subject / kicker from content["kinds"]
    (falls back to content["kinds"]["default"]).

content.json: see assets/example_content.json. Paragraph strings may contain
"{OFFER}" (replaced by the kind's offer sentence) and "{AUDIENCE}".

Writes out_dir/<n>.json  ({"to":[...],"subject":...,"body":...,"htmlBody":...})
and out_dir/<n>.html (preview). Links are plain underlined text: coloured
button backgrounds disappear in Gmail mobile.
"""
import html
import json
import os
import sys

P, G, BG = "#5b3f7a", "#6f9a3f", "#f4f1f7"
e = html.escape


def build(content, r):
    kinds = content["kinds"]
    k = kinds.get(r.get("kind", "default"), kinds["default"])
    greet = f"שלום {r['greeting_name']}," if r.get("greeting_name") else f"שלום {r.get('team_label', 'לצוות')},"
    paras = [p.replace("{OFFER}", k["offer"]).replace("{AUDIENCE}", k.get("audience", "")) for p in content["paragraphs"]]
    sig = content["signature"]
    card = content["card"]
    links = content["links"]

    h = [f'<div dir="rtl" style="direction:rtl;text-align:right;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.7;color:#222;max-width:680px">',
         f"<p>{e(greet)}</p>"]
    h += [f"<p>{e(p)}</p>" for p in paras]
    h.append("<p>" + "<br>".join(e(s) for s in sig) + "</p>")
    h.append(f'<div style="margin-top:28px;border-top:6px solid {G};background:#fff;border:1px solid #e3dcea;border-radius:8px;padding:22px 24px">')
    h.append(f'<div style="font-size:12px;color:#777">{e(k.get("kicker", card.get("kicker", "")))}</div>')
    h.append(f'<h2 style="margin:10px 0 4px;color:{P};font-size:24px">{e(card["title"])}</h2>')
    h.append(f'<div style="color:{G};font-weight:bold">{e(card["subtitle"])}</div>')
    for sec in card["sections"]:
        h.append(f'<h3 style="color:{P};margin:18px 0 6px">{e(sec["heading"])}</h3>')
        if "boxes" in sec:  # 2-column grid of small boxes
            h.append('<table role="presentation" dir="rtl" width="100%" cellpadding="0" cellspacing="8" style="border-collapse:separate">')
            bx = sec["boxes"]
            for i in range(0, len(bx), 2):
                h.append("<tr>")
                for t, d in bx[i:i + 2]:
                    h.append(f'<td valign="top" width="50%" style="background:{BG};border-radius:6px;padding:10px 12px;text-align:right"><b style="color:{P}">{e(t)}</b><br><span style="font-size:14px">{e(d)}</span></td>')
                h.append("</tr>")
            h.append("</table>")
        for item in sec.get("items", []):  # [title, text]
            h.append(f'<p style="margin:6px 0"><b style="color:{P}">{e(item[0])}</b><br>{e(item[1])}</p>')
        if sec.get("text"):
            h.append(f'<p style="margin:0">{e(sec["text"])}</p>')
    if card.get("footnote_html"):
        h.append(f'<p style="font-size:12px;color:#666;margin:10px 0 0">{card["footnote_html"]}</p>')
    lnk = f"color:{P};font-weight:bold;text-decoration:underline"
    h.append(f'<div style="margin-top:20px;background:{BG};border-radius:8px;padding:16px 18px">')
    h.append(f'<b style="color:{P}">{e(content["contact_title"])}</b><br>{e(content["contact_line"])}<div style="margin-top:12px">')
    for icon, label, url in links:
        h.append(f'<p style="margin:0 0 4px">{icon} <a href="{e(url)}" style="{lnk}">{e(label)}</a></p>')
    h.append("</div></div></div></div>")

    txt = [greet, ""] + sum([[p, ""] for p in paras], []) + sig + ["", "—"]
    for sec in card["sections"]:
        for item in sec.get("items", []):
            txt.append(f"{item[0]}: {item[1]}")
    txt.append("")
    txt += [f"{label}: {url}" for _, label, url in links]
    return {"to": [r["email"]], "subject": k["subject"], "body": "\n".join(txt), "htmlBody": "".join(h)}


def main():
    content = json.load(open(sys.argv[1], encoding="utf-8"))
    recips = json.load(open(sys.argv[2], encoding="utf-8"))
    out = sys.argv[3]
    os.makedirs(out, exist_ok=True)
    for i, r in enumerate(recips):
        msg = build(content, r)
        json.dump(msg, open(os.path.join(out, f"{i}.json"), "w", encoding="utf-8"), ensure_ascii=False)
        open(os.path.join(out, f"{i}.html"), "w", encoding="utf-8").write(
            '<!doctype html><meta charset="utf-8"><body style="background:#eee;padding:20px">' + msg["htmlBody"])
        print(i, msg["to"][0], msg["body"].split("\n")[0])


if __name__ == "__main__":
    main()
