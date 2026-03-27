<script lang="ts">
  import type { ApplicationStatus } from "$lib/types.js";
  import { statusLabel, statusClasses } from "$lib/utils/helpers.js";
  let { status }: { status: ApplicationStatus } = $props();
</script>

<span
  style="font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 999px; border: 1px solid; {statusClasses(
    status,
  )}"
>
  {statusLabel(status)}
</span>
