/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        butai: {
          dark: '#1c130d',
          wood: '#3b2219',
          lightWood: '#6e473b',
          brass: '#d4af37',
          brassHover: '#e6c760',
          paper: '#fcf8ee',
          vermilion: '#c83c23',
          indigo: '#1b2a4a',
        }
      },
      fontFamily: {
        serif: ['Georgia', 'Cambria', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'stage': '0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 100px rgba(0, 0, 0, 0.5) inset',
        'wood': 'inset 0 2px 4px rgba(255, 255, 255, 0.1), inset 0 -4px 8px rgba(0, 0, 0, 0.6)',
      }
    },
  },
  plugins: [],
}
