# MatchBeforeApply FAQ

Source of truth for the FAQ chatbot. Each entry needs a stable `id` that survives
edits to its text — ids are never reused. Editing an answer re-embeds only that entry.

### [id: what-is-this]
**What does MatchBeforeApply do?**
It compares your CV against a job description and gives you a match score plus
practical tips for applicant tracking systems. You upload your CV once, then paste a
job description whenever you want to check a role.

### [id: getting-started]
**How do I get started?**
Sign in, or create an account when sign-up is enabled, then upload your CV as a PDF on
the profile page. Create an application by pasting a job description or its URL and
leave “Run analysis immediately” enabled to analyze and save it.

### [id: cv-upload]
**How do I upload my CV?**
Go to your profile page and upload a PDF. The text is extracted and stored on your
profile, so you only need to do this once — every later analysis reuses it.

### [id: cv-format]
**What file formats can I upload for my CV?**
The CV upload supports PDF files. The text is extracted from the PDF and saved as plain
text. If your CV is a Word document or an image, export it to PDF first.

### [id: cv-replace]
**Can I change or update my CV later?**
Yes. Upload a new PDF on the profile page at any time and it replaces the CV text
stored on your profile. Later analyses use the replacement automatically.

### [id: cv-storage]
**What happens to my CV after I upload it?**
The app reads the uploaded PDF, extracts its text, and stores that text on your
profile for analyses. The upload endpoint does not save the original PDF file.

### [id: job-description-input]
**Can I paste a job description URL instead of the text?**
Yes. The new application form accepts either a URL or the raw job-description text.
Sites that require a login or block automated access may not work, so paste the text
directly in those cases.

### [id: match-score-meaning]
**How is the match score calculated?**
The app compares the skills and experience extracted from your CV with the job
requirements. Skills contribute 60 percent and experience 40 percent to the overall
0–10 score. Results also show matched and missing skills and a short summary.

### [id: good-score]
**What counts as a good match score?**
The scoring guide treats 9–10 as exceptional, 7–8 as strong, 5–6 as moderate, 3–4 as
weak, and 1–2 as poor. Treat the score as guidance about how your stated skills and
experience match the posting, not as a hiring decision.

### [id: missing-skills]
**What should I do about the missing skills it lists?**
Check whether your CV describes relevant experience with different wording. If it
does, clarify that real experience using standard terminology from the posting. If
you do not have a listed skill, do not add it as though you do.

### [id: ats-tips]
**What are the ATS tips?**
The tips help present experience you genuinely have more clearly. They can recommend
standard terminology, quantified achievements, highlighting relevant experience, or
genuine learning for a missing required skill; they should never suggest faking one.

### [id: analysis-limit]
**Is there a limit on how many analyses I can run?**
Yes. Regular accounts can run three analyses per day, and the counter resets on a new
day. The shared demo account is exempt from this limit and uses mock analysis data.

### [id: analysis-time]
**How long does an analysis take?**
There is no fixed completion-time guarantee because processing can depend on the job
description and model response. While it runs, the app shows progress as it reads the
description, parses your CV, scores the match, and generates insights.

### [id: applications-board]
**How do I track the jobs I have applied to?**
Applications are saved as cards on your board, including ones created for an immediate
analysis. You can search by job title or company and move cards between status columns
as your applications progress.

### [id: application-status]
**What are the application statuses?**
The board stages are Open/Prepare to Apply, Applied, In Progress, and Rejected/Closed.
You set a card’s stage yourself, either from its application page or by moving it to
another board column.

### [id: comments]
**Can I keep notes on an application?**
Yes. Each application has a comment timeline. Comments are typed as general, company,
interview, or Q&A, so you can keep interview questions separate from company research.

### [id: cover-letter]
**Can I store a cover letter with an application?**
Yes. Each application has a cover-letter field you can fill in and edit. It is saved
with that application alongside the job details and match results.

### [id: rerun-analysis]
**Can I re-run the analysis on a saved application?**
Yes. Open the saved application and select “Run Analysis” or “Re-run Analysis.” This
uses your currently stored CV, so it is useful after replacing your CV.

### [id: delete-application]
**How do I delete an application?**
Open the application, select Delete, and confirm the deletion. The application and its
comments are removed together, and the app does not provide an undo action.

### [id: sign-in-google]
**Can I sign in with Google?**
Yes, when Google sign-in is configured for the deployment. A new account created
through Google has no separate app password; an existing email-and-password account
linked to Google keeps its existing sign-in method.

### [id: data-privacy]
**Who can see my CV and applications?**
Other users cannot access them. Profile, application, and comment endpoints require a
login and scope records to the signed-in account, so one account cannot retrieve
another account’s CV, applications, or comments through the app.

### [id: chatbot-scope]
**What can this chat answer?**
It answers questions about how MatchBeforeApply works, including CV uploads, scores,
application tracking, and accounts. It cannot review your CV, assess a particular
employer or job, or answer unrelated general questions, so it refuses those requests.
