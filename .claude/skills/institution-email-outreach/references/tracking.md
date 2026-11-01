# Tracking sheet

Columns (Hebrew, one row per institution):
`# | סוג גוף | גוף / רשות | נמען | תפקיד | מייל | העתק | תאריך שליחה | נושא המייל | סטטוס שליחה | הערות שליחה | טלפון | מקור הכתובת | תשובה התקבלה? | תאריך תשובה | תוכן התשובה | פעולה הבאה | תאריך לפעולה הבאה | הערות`

Status values: נשלח / חזר (550) / לא נשלח – [סיבה].
Response values: כן – חיובית / כן – שלילית / אישור קבלה אוטומטי / —.

Notes:
- Dates as YYYY-MM-DD. Phones written as `="08-1234567"` in CSV so Sheets keeps the leading zero.
- Creating a new sheet: upload CSV via Drive `create_file` (contentMimeType text/csv) — it converts to a Google Sheet. Editing an existing sheet needs the Google Sheets connector; without it, give tab-separated rows to paste.
- Keep a local CSV copy in the scratchpad and append after each round.
