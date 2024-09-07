/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#F7F7F7', // Light Gray for background
        surface: '#FFFFFF', // Pure White for cards
        text: {
          primary: '#333333', // Dark Gray for primary text
          secondary: '#B0B0B0', // Medium Gray for secondary text
          accent: '#1C1C1C', // Rich Black for accents
        },
      },
    },
  },
  plugins: [],
}
