/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: ["tailwindcss ,autoprefixer", require("flowbite/plugin")],
  darkMode: "class",
};
