# MatchBeforeApply FAQ

Source of truth for the FAQ chatbot. Each entry needs a stable `id` that survives
edits to its text — ids are never reused. Editing an answer re-embeds only that entry.

### [id: what-is-this]
**What does MatchBeforeApply do?**
It compares your CV against a job description and gives you a match score plus
practical tips for applicant tracking systems. You upload your CV once, then paste a
job description whenever you want to check a role.

### [id: problem-solved]
**Which problem does this app solve? How do I benefit from using it?**
It solves two problems: keeping track of every job you've applied to, and knowing
whether a role is actually worth applying to in the first place, through the match
score and ATS insights. The ATS insights specifically catch cases where you already
have a skill the job asks for, but your CV describes it with different wording.

### [id: why-not-llm]
**Why should I use this instead of just asking a general-purpose LLM to compare my CV and the job?**
A general LLM can do a one-off comparison, but it won't remember your CV between
conversations, won't score it the same consistent way every time, and won't save
the result anywhere. MatchBeforeApply stores your CV once, applies the same
skills/experience scoring method every time, and keeps every analysis attached to a
tracked application so you can compare roles and follow up later, rather than
starting over in a new chat each time.

### [id: who-built-this]
**Who built and maintains MatchBeforeApply?**
It was built by Naji, who started the project while job
hunting, needed this exact tool himself, and built it so other job seekers could use
it too.

### [id: getting-started]
**How do I get started?**
Sign in, or create an account when sign-up is enabled, then upload your CV as a PDF on
the profile page. Create an application by pasting a job description or its URL and
leave “Run analysis immediately” enabled to analyze and save it.

### [id: skip-analysis]
**Can I create an application without running analysis right away?**
Yes. Turn off “Run analysis immediately” when creating the application to save it
without analyzing. You can trigger the analysis at any time afterward from the
application page.

### [id: email-verification]
**Do I need to verify my email before I can run an analysis?**
Yes. Your email must be verified before you can run an analysis. Check your inbox
for the verification link after you sign up.

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

### [id: cv-multiple]
**Can I upload multiple CVs, for example one per job type?**
No. The app stores only one CV at a time. Uploading a new PDF replaces the previous
one, and every analysis — including re-analyzing an older saved application — uses
your most recently uploaded CV, not the CV that was in place when that application
was first created.

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
The ATS insights specifically catch cases where you already
have a skill the job asks for, but your CV describes it with different wording —
fixing that wording helps both human readers and the AI/ATS tools recruiters use to
screen CVs.

### [id: analysis-limit]
**Is there a limit on how many analyses I can run?**
Yes. Regular accounts can run three analyses per day, and the counter resets on a new
day. The shared demo account is exempt from this limit and uses mock analysis data.

### [id: pricing]
**Is MatchBeforeApply free?**
Yes. The app is currently free to use, with a limit of three analyses per day per
account. There are no paid plans at this time.

### [id: self-hosted]
**Does the self-hosted version have the same features?**
Yes, with one exception. The self-hosted version includes every core feature — CV
analysis, match scoring, ATS tips, and application tracking — but does not include
this FAQ chatbot.

### [id: self-host-instructions]
**How can I self-host MatchBeforeApply?**
Go to the project's GitHub repository at github.com/Naji-k/MatchBeforeApply and
follow the "Getting Started" section in the README.

### [id: self-host-requirements]
**Is it easy to self-host?**
Yes. You need Docker Compose and a Google AI (Gemini) API key. It's a ready-to-run
product — running the setup script brings everything up.

### [id: contribute]
**Can I contribute to this project?**
Yes. Feel free to fork the repository and open a pull request — even small fixes
like documentation, typos, or refactors are welcome.

### [id: why-multiple-agents]
**Why does this app use 4 separate agents instead of one?**
Each agent has one narrow, well-defined job with its own focused prompt, which keeps
its instructions simpler and its output more reliable than asking one agent to do
everything at once.

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

### [id: edit-job-description]
**Can I edit a job description after saving it?**
No. The job description text is stored with the application when it's created and
can't be edited afterward. Re-running the analysis re-scores that same saved job
description against your current CV; it doesn't let you change the job description
itself. To analyze a different job description, create a new application.

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

### [id: data-sharing]
**Does the app share my CV or applications with anyone?**
No. The app does not share your CV or applications with any third party. It uses your
CV text to generate match scores and insights.

### [id: data-retention]
**How long does the app keep my CV and applications?**
The app keeps your CV and applications until you delete them. The app does not
automatically delete them after a period of time.

### [id: training-data]
**Does the app use my CV or applications to train its models?**
No. The app does not use your CV or applications to train its models. It uses your
CV text to generate match scores and insights, but it does not store your CV or
applications for model training.

### [id: data-security]
**How does the app protect my CV and applications?**
The app protects your CV and applications with standard security practices, including HTTPS for data in transit, secure storage for data at rest, and access controls to ensure that only you can access your data.

### [id: sharing-with-others]
**Can I share my CV or applications with others?**
No. The app does not provide a feature to share your CV or applications with others. Your data is private and can only be accessed by you when logged into your account.

### [id: account-deletion]
**What happens if I delete my account?**
When you delete your account, all your CVs, applications, and comments are permanently removed from the system. This action cannot be undone, so make sure you want to delete your account before proceeding.

### [id: greeting]
**what if someone is just looking for a greeting?**
The chatbot can respond to greetings, but it will also remind users that it is designed to answer questions about MatchBeforeApply and its features.

### [id: ownership]
**Who owns the data I provide to the app?**
You retain ownership of your CV and applications. The app acts as a service provider that processes your data to provide the features you use, but it does not claim ownership of your content.

### [id: download-data]
**Can I download my CV and applications?**
No. The app does not currently provide a feature to download your CV or applications.

### [id: access-to-data]
**Can I access my CV and applications from multiple devices?**
Yes. You can access your CV and applications from any device by logging into your account.

### [id: support]
**How can I get support if I have issues with the app?**
You can use feedback buttons in the app to report issues or ask questions.

### [id: feedback]
**How can I provide feedback on the app?**
You can provide feedback through the app's feedback feature, which allows you to submit comments, suggestions, or report bugs directly to the development team.

### [id: generate-cover-letter]
**Can the app help me generate a cover letter?**
No, the app does not provide a feature to generate cover letters. It focuses on analyzing your CV against job descriptions and providing match scores and insights.

### [id: generate-resume]
**Can the app help me generate a resume?**
Currently, the app does not provide a feature to generate resumes, but soon it will be able to generate a resume.

### [id: tech-stack]
**What tech stack does MatchBeforeApply use?**
The AI pipeline runs on Google ADK. The backend is FastAPI with async SQLAlchemy and PostgreSQL, using JWT and argon2 for authentication. 
The frontend is SvelteKit with TypeScript and Tailwind CSS. The whole stack is Dockerized and served through Caddy.
