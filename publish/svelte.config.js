import adapter from "@sveltejs/adapter-static";

/** @type {import('@sveltejs/kit').Config} */

const config = {
  kit: {
    adapter: adapter({
      out: "build",
      precompress: false,
      fallback: "index.html",
    }),
    files: {
      assets: "assets",
    },
  },
};

export default config;
