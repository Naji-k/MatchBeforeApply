<script lang="ts">
  import { goto } from "$app/navigation";
  import { createApplication, streamAnalysis, ApiError } from "$lib/api.js";
  import LoadingSteps from "$lib/components/LoadingSteps.svelte";
  import { authStore, showToast, incrementUsage } from "$lib/stores";
  import { trackEvent } from "$lib/utils/analytics";

  let jdMode = $state<"text" | "url">("text");
  let jdText = $state("");
  let jdUrl = $state("");
  let jobPostingUrl = $state("");
  let runAnalysis = $state(true);
  let loading = $state(false);
  let error = $state("");
  let currentStep = $state(-1);
  let doneSteps = $state(new Set<number>());

  async function handleSubmit(e: SubmitEvent): Promise<void> {
    e.preventDefault();
    error = "";
    const jdSource = jdMode === "text" ? jdText.trim() : jdUrl.trim();
    const jobUrl =
      jdMode === "url" ? jdUrl.trim() : jobPostingUrl.trim() || undefined;
    if (!jdSource) {
      error = "Please provide a job description.";
      return;
    }
    if ($authStore.user?.id == import.meta.env.VITE_DEMO_USER) {
      showToast(
        "You're using the demo account 👀 Results are mock data.",
        "info",
      );
      trackEvent("demo_new_application_click");
    } else {
      incrementUsage();
      trackEvent("new_application_click");
    }
    loading = true;
    try {
      const app = await createApplication({
        jd_source: jdSource,
        jd_type: jdMode,
        jd_url: jobUrl,
        run_analysis: false,
      });

      if (runAnalysis) {
        for await (const event of streamAnalysis(app.id)) {
          if (event.type === "step_start") {
            currentStep = event.step;
          } else if (event.type === "step_done") {
            doneSteps = new Set([...doneSteps, event.step]);
            currentStep = -1;
          } else if (event.type === "done") {
            goto(`/applications/${app.id}`);
            return;
          } else if (event.type === "error") {
            if (event.status_code === 403) {
              loading = false;
              currentStep = -1;
              doneSteps = new Set();
              error =
                "Please verify your email before running analyses. Go to Profile to verify.";
              return;
            }
            throw new Error(event.message);
          }
        }
      } else {
        goto(`/applications/${app.id}`);
      }
    } catch (err) {
      loading = false;
      currentStep = -1;
      doneSteps = new Set();
      error =
        err instanceof ApiError && err.status === 422
          ? "Please upload your CV before running analysis."
          : (err as Error).message;
    }
  }
</script>

<svelte:head><title>New Application — CV Matcher</title></svelte:head>

{#if loading && runAnalysis}
  <LoadingSteps
    running={true}
    activeStep={currentStep}
    {doneSteps}
    controlled={true}
  />
{:else if !loading}
  <div style="max-width:680px;margin:0 auto;padding:2rem 1rem">
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem">
      <a
        href="/applications"
        style="color:var(--color-text-muted);font-size:.875rem;text-decoration:none"
        >← Back</a
      >
      <h1 style="font-size:1.6rem;font-weight:700">New Application</h1>
    </div>

    <form
      class="card"
      style="display:flex;flex-direction:column;gap:1.4rem;padding:1.5rem;"
      onsubmit={handleSubmit}
    >
      {#if error}
        <div
          style="background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);color:#f87171;font-size:.875rem;padding:.75rem 1rem;border-radius:10px"
        >
          {error}
        </div>
      {/if}

      <!-- JD toggle -->
      <div style="display:flex;flex-direction:column;gap:.5rem">
        <span
          style="font-size:.85rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em"
        >
          Job Description
        </span>
        <div style="display:flex;gap:.5rem">
          {#each [{ value: "text" as const, label: "Paste Text" }, { value: "url" as const, label: "URL" }] as mode}
            <button
              type="button"
              style="
                padding:.45rem 1.2rem;border-radius:8px;border:1px solid;
                font-size:.9rem;cursor:pointer;transition:all .2s;
                {jdMode === mode.value
                ? 'background:var(--color-accent);border-color:var(--color-accent);color:#fff'
                : 'background:transparent;border-color:var(--color-border);color:var(--color-text-muted)'}
              "
              onclick={() => (jdMode = mode.value)}
            >
              {mode.label}
            </button>
          {/each}
        </div>
      </div>

      {#if jdMode === "text"}
        <textarea
          class="input-field"
          rows="8"
          placeholder="Paste the job description here…"
          style="resize:vertical"
          bind:value={jdText}
        ></textarea>
        <!-- Job Posting URL -->
        <div style="display:flex;flex-direction:column;gap:.5rem">
          <label
            for="job-posting-url"
            style="font-size:.85rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em"
          >
            Job Posting URL <span style="font-weight:400;opacity:.6"
              >(optional)</span
            >
          </label>
          <input
            id="job-posting-url"
            type="url"
            class="input-field"
            placeholder="https://…"
            bind:value={jobPostingUrl}
          />
        </div>
      {:else}
        <span style="font-size:.85rem;color:red;font-style:italic">
          ⚠️ URLs may not work on sites that require login. For best
          results,paste the job description text directly.
        </span>
        <input
          type="url"
          class="input-field"
          placeholder="https://…"
          bind:value={jdUrl}
        />
      {/if}

      <!-- Run analysis toggle -->
      <div
        style="display:flex;align-items:center;gap:.75rem;cursor:pointer;user-select:none"
        onclick={() => (runAnalysis = !runAnalysis)}
        onkeydown={(e) => e.key === " " && (runAnalysis = !runAnalysis)}
        role="presentation"
      >
        <div
          style="
            position:relative;width:2.5rem;height:1.5rem;border-radius:999px;border:1px solid;
            transition:all .2s;flex-shrink:0;
            {runAnalysis
            ? 'background:var(--color-accent);border-color:var(--color-accent)'
            : 'background:var(--color-surface-2);border-color:var(--color-border)'}
          "
          role="checkbox"
          aria-checked={runAnalysis}
          tabindex="0"
          onkeydown={(e) => e.key === " " && (runAnalysis = !runAnalysis)}
        >
          <div
            style="
            position:absolute;top:.2rem;width:1rem;height:1rem;background:#fff;border-radius:50%;transition:left .2s;
            {runAnalysis ? 'left:1.2rem' : 'left:.2rem'}
          "
          ></div>
        </div>
        <span style="font-size:.9rem;color:var(--color-text-primary)"
          >Run analysis immediately</span
        >
      </div>

      <div style="display:flex;gap:.75rem;padding-top:.25rem">
        <button type="submit" class="btn-primary" style="flex:1;padding:.9rem">
          {runAnalysis ? "Analyze" : "Save Application"}
        </button>
        <a
          href="/applications"
          class="btn-secondary"
          style="padding:.9rem 1.5rem;text-decoration:none;display:inline-flex;align-items:center"
        >
          Cancel
        </a>
      </div>
    </form>
  </div>
{/if}
