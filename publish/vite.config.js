import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import adapter from "@sveltejs/adapter-static";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    sveltekit({
      adapter: adapter({
        out: "build",
        precompress: false,
        fallback: "index.html",
      }),
      files: {
        assets: "assets",
      },
    }),
    tailwindcss(),
  ],
  server: {
    allowedHosts: [
      "matchbeforeapply.up.railway.app",
      "matchbeforeapply.com",
      "www.matchbeforeapply.com",
    ],
  },
});
