/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        kiosk: [
          "Hind Siliguri",
          "system-ui",
          "Segoe UI",
          "sans-serif",
        ],
      },
      colors: {
        brand: {
          ocean: "#0e7490",
          sand: "#f59e0b",
          night: "#0f172a",
        },
      },
    },
  },
  plugins: [],
};
