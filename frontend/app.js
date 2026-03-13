// ── View helpers ──────────────────────────────────────
const views = {
  upload: document.getElementById("upload-view"),
  loading: document.getElementById("loading-view"),
  results: document.getElementById("results-view"),
};

function showView(name) {
  Object.entries(views).forEach(([k, el]) => {
    el.classList.toggle("active", k === name);
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ── File drop ─────────────────────────────────────────
const fileDrop = document.getElementById("file-drop");
const fileInput = document.getElementById("cv-file");
const fileLabel = document.getElementById("file-label");

fileDrop.addEventListener("click", () => fileInput.click());

fileDrop.addEventListener("dragover", (e) => {
  e.preventDefault();
  fileDrop.classList.add("dragover");
});
fileDrop.addEventListener("dragleave", () =>
  fileDrop.classList.remove("dragover"),
);
fileDrop.addEventListener("drop", (e) => {
  e.preventDefault();
  fileDrop.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  if (file) setFile(file);
});

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

function setFile(file) {
  fileLabel.textContent = `📄 ${file.name}`;
  fileDrop.classList.add("has-file");
}

// ── JD toggle ─────────────────────────────────────────
let jdMode = "text";

document.querySelectorAll(".toggle-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    jdMode = btn.dataset.mode;
    document
      .querySelectorAll(".toggle-btn")
      .forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    document
      .getElementById("jd-text-field")
      .classList.toggle("hidden", jdMode !== "text");
    document
      .getElementById("jd-url-field")
      .classList.toggle("hidden", jdMode !== "url");
  });
});

// ── Loading steps ─────────────────────────────────────
const STEPS = [
  { id: "step-jd", label: "📋 Reading job description", ms: 800 },
  { id: "step-cv", label: "📄 Parsing your CV", ms: 1600 },
  { id: "step-match", label: "🎯 Scoring the match", ms: 2400 },
  { id: "step-ats", label: "🔍 Generating ATS tips", ms: 3200 },
];

let stepTimers = [];

function startSteps() {
  STEPS.forEach((s) =>
    document.getElementById(s.id)?.classList.remove("active", "done"),
  );
  stepTimers.forEach(clearTimeout);
  stepTimers = [];

  STEPS.forEach((s, i) => {
    const t1 = setTimeout(() => {
      STEPS.forEach((x) =>
        document.getElementById(x.id)?.classList.remove("active"),
      );
      document.getElementById(s.id)?.classList.add("active");
    }, s.ms);

    const t2 = setTimeout(
      () => {
        document.getElementById(s.id)?.classList.remove("active");
        document.getElementById(s.id)?.classList.add("done");
      },
      s.ms + (STEPS[i + 1]?.ms - s.ms || 800) - 100,
    );

    stepTimers.push(t1, t2);
  });
}

function finishSteps() {
  stepTimers.forEach(clearTimeout);
  STEPS.forEach((s) => {
    const el = document.getElementById(s.id);
    el?.classList.remove("active");
    el?.classList.add("done");
  });
}

// ── Form submit ───────────────────────────────────────
document
  .getElementById("analyze-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const cvFile = fileInput.files[0];
    if (!cvFile) {
      alert("Please select a PDF file.");
      return;
    }

    const jdInput =
      jdMode === "text"
        ? document.getElementById("jd-text").value.trim()
        : document.getElementById("jd-url").value.trim();

    if (!jdInput) {
      alert("Please provide a job description.");
      return;
    }

    showView("loading");
    startSteps();

    const form = new FormData();
    form.append("cv_file", cvFile);
    form.append("jd_type", jdMode);
    form.append("jd_input", jdInput);

    try {
      const res = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        body: form,
      });

      // Always read as text first so a non-JSON body doesn't silently throw
      const text = await res.text();

      if (!res.ok) {
        let errMsg = `Server error (${res.status})`;
        try {
          errMsg = JSON.parse(text).detail || errMsg;
        } catch {}
        throw new Error(errMsg);
      }

      let data;
      try {
        data = JSON.parse(text);
        console.log(data);
      } catch {
        // Show raw server response so we can debug
        throw new Error(`Server returned invalid JSON:\n${text.slice(0, 500)}`);
      }

      finishSteps();
      setTimeout(() => renderResults(data), 400);
    } catch (err) {
      finishSteps();
      alert(`Error: ${err.message}`);
      console.error(err);
      showView("upload");
    }
  });

// ── Render results ────────────────────────────────────
function renderResults(data) {
  console.log("Rendering results with data:\n", data);
  const match = data.match_result || {};
  const ats = data.ats_tips || {};

  // Overall ring
  const overall = match.overall_score ?? 0;
  document.getElementById("overall-score-val").textContent = overall;
  const circumference = 314;
  const offset = circumference - (overall / 10) * circumference;
  const ringFill = document.getElementById("ring-fill");

  // Colour ring by score
  const colour =
    overall >= 7 ? "#4ade80" : overall >= 4 ? "#facc15" : "#f87171";
  ringFill.style.stroke = colour;

  setTimeout(() => {
    ringFill.style.strokeDashoffset = offset;
  }, 50);

  // Skill / experience bars
  const skillsScore = match.skills_score ?? 0;
  const expScore = match.experience_score ?? 0;
  document.getElementById("skills-score-val").textContent = `${skillsScore}/10`;
  document.getElementById("exp-score-val").textContent = `${expScore}/10`;
  setTimeout(() => {
    document.getElementById("skills-bar").style.width = `${skillsScore * 10}%`;
    document.getElementById("exp-bar").style.width = `${expScore * 10}%`;
  }, 50);

  // Summary
  document.getElementById("match-summary").textContent = match.summary || "—";

  // Skills chips
  renderChips("matched-skills", match.matched_skills || [], "chip-green");
  renderChips("missing-skills", match.missing_skills || [], "chip-red");

  // ATS tips
  const tipsList = document.getElementById("ats-tips-list");
  tipsList.innerHTML = "";
  const tips = ats.tips || [];
  tips.forEach((tip) => {
    const li = document.createElement("li");
    li.textContent = tip;
    tipsList.appendChild(li);
  });

  if (!tips.length) {
    const li = document.createElement("li");
    li.textContent = "No tips generated.";
    tipsList.appendChild(li);
  }

  showView("results");
}

function renderChips(containerId, items, chipClass) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  if (!items.length) {
    container.innerHTML =
      '<span style="color:var(--muted);font-size:.85rem">None</span>';
    return;
  }
  items.forEach((item) => {
    const span = document.createElement("span");
    span.className = `chip ${chipClass}`;
    span.textContent = item;
    container.appendChild(span);
  });
}

// ── Start over ────────────────────────────────────────
document.getElementById("start-over-btn").addEventListener("click", () => {
  // document.getElementById("analyze-form").reset();
  fileLabel.textContent = "Click or drag your PDF here";
  fileDrop.classList.remove("has-file");
  showView("upload");
});
