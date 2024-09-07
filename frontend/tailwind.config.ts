/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      container: {
        center: true,
        padding: "1rem",
      },
      colors: {
        primary: "#4A90E2", // Soft Blue
        secondary: "#007BFF", // Muted Blue
        background: "#E3F2FD", // Light Blue
        surface: "#FFFFFF", // White for cards
        text: {
          primary: "#333333", // Dark Gray for primary text
          secondary: "#666666", // Medium Gray for secondary text
        },
      },
    },
  },
  plugins: [],
};
