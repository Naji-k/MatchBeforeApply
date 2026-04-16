<script lang="ts">
  import { verifyEmail, sendVerification } from "$lib/api.js";
  import { setEmailVerified, showToast } from "$lib/stores.js";

  let { email, onVerified }: { email: string; onVerified: () => void } =
    $props();

  let otpValue = $state("");
  let verifying = $state(false);
  let resending = $state(false);

  async function handleVerify() {
    verifying = true;
    try {
      await verifyEmail(otpValue.trim());
      setEmailVerified();
      otpValue = "";
      showToast("Email verified!", "success");
      onVerified();
    } catch (err) {
      showToast((err as Error).message);
    } finally {
      verifying = false;
    }
  }

  async function handleResend() {
    resending = true;
    try {
      await sendVerification();
      showToast("New code sent — check your email.", "info");
    } catch (err) {
      showToast((err as Error).message);
    } finally {
      resending = false;
    }
  }
</script>

<div class="card" style="padding:.75rem;border-left:3px solid #f59e0b">
  <p
    style="font-size:.8rem;font-weight:600;color:#b45309;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem"
  >
    Email Verification Required
  </p>
  <p style="font-size:.9rem;color:var(--color-text-muted);margin-bottom:.75rem">
    Enter the 6-digit code sent to <strong>{email}</strong>. You must verify
    your email to run analyses.
  </p>
  <div style="display:flex;flex-direction:column;gap:.5rem;margin-bottom:.6rem">
    <input
      type="text"
      inputmode="numeric"
      maxlength="6"
      placeholder="123456"
      bind:value={otpValue}
      style="padding:.5rem .75rem;border:1px solid var(--color-border);border-radius:8px;font-size:1.2rem;letter-spacing:.25em;text-align:center;background:var(--color-surface);color:var(--color-text-primary)"
    />
    <button
      class="btn-primary"
      onclick={handleVerify}
      disabled={verifying || otpValue.length < 6}
      style="padding:.5rem 1.25rem;width:100%"
    >
      {verifying ? "Verifying…" : "Verify"}
    </button>
  </div>
  <button
    onclick={handleResend}
    disabled={resending}
    style="background:none;border:none;font-size:.82rem;color:var(--color-text-muted);cursor:pointer;padding:0;text-decoration:underline"
  >
    {resending ? "Sending…" : "Resend code"}
  </button>
</div>
