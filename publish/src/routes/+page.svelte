<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import { authStore } from "$lib/stores.js";

  import LandingNav from "$lib/components/landing/LandingNav.svelte";
  import Hero from "$lib/components/landing/Hero.svelte";
  import TrustStrip from "$lib/components/landing/TrustStrip.svelte";
  import ProblemSection from "$lib/components/landing/ProblemSection.svelte";
  import HowItWorks from "$lib/components/landing/HowItWorks.svelte";
  import FeatureGrid from "$lib/components/landing/FeatureGrid.svelte";
  import SampleReport from "$lib/components/landing/SampleReport.svelte";
  import FounderStory from "$lib/components/landing/FounderStory.svelte";
  import FinalCta from "$lib/components/landing/FinalCta.svelte";
  import SiteFooter from "$lib/components/landing/SiteFooter.svelte";

  onMount(() => {
    if (get(authStore).isAuthenticated) {
      goto("/applications");
    }
  });
</script>

<svelte:head>
  <title>Match Before Apply — Know your match before you apply</title>
  <meta
    name="description"
    content="Upload your CV, paste a job description or job post URL, and get a clear match score, key gaps, and ATS insights — then track every application in one place."
  />
</svelte:head>

<LandingNav />
<Hero />
<TrustStrip />
<ProblemSection />
<HowItWorks />
<FeatureGrid />
<SampleReport />
<FounderStory />
<FinalCta />
<SiteFooter />
