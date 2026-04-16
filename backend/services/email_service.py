import resend

from core.config import settings


def send_feedback_email(user_name: str, user_email: str, message: str) -> None:
    resend.api_key = settings.RESEND_TOKEN
    resend.Emails.send(
        {
            "from": settings.RESEND_FROM_EMAIL,
            "to": ["support@matchbeforeapply.com"],
            "subject": f"Feedback from {user_name}",
            "html": f"""
                <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 2rem;">
                  <h1 style="font-size: 1.5rem; font-weight: 800; letter-spacing: -1px">
                    Match Before <span style="color: #2563eb">Apply</span>
                  </h1>
                  <h2 style="margin-bottom: 0.5rem">New Feedback</h2>
                  <p style="color: #555;"><strong>From:</strong> {user_name} ({user_email})</p>
                  <div style="background: #f4f4f5; border-radius: 10px; padding: 1rem 1.5rem; margin-top: 1rem;">
                    <p style="white-space: pre-wrap; margin: 0;">{message}</p>
                  </div>
                </div>
            """,
        }
    )


def send_otp_email(to: str, otp: str) -> None:
    resend.api_key = settings.RESEND_TOKEN
    resend.Emails.send(
        {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [to],
            "subject": "Your verification code — Match Before Apply",
            "html": f"""
                    <div
                      style="
                        font-family: sans-serif;
                        max-width: 480px;
                        margin: 0 auto;
                        padding: 2rem;
                      "
                    >
                      <h1 style="font-size: 2rem; font-weight: 800; letter-spacing: -1px">
                        Match Before
                        <span style="color: #2563eb">Apply</span>
                      </h1>
                      <h2 style="margin-bottom: 0.5rem">Verify your email</h2>
                      <p style="color: #555; margin-bottom: 1.5rem">
                        Use the code below to verify your account. It expires in
                        <strong>10 minutes</strong>.
                      </p>
                      <div
                        style="
                          font-size: 2rem;
                          font-weight: 700;
                          letter-spacing: 0.3em;
                          background: #f4f4f5;
                          border-radius: 10px;
                          padding: 1rem 1.5rem;
                          text-align: center;
                          margin-bottom: 1.5rem;
                        "
                      >
                        {otp}
                      </div>
                      <p style="color: #999; font-size: 0.85rem">
                        If you did not create an account, you can ignore this email.
                      </p>
                    </div>

            """,
        }
    )
