/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../**/templates/**/*.html',
    '../**/*.py',
  ],
  theme: {
    extend: {
      fontFamily: {
          'oswald': ['Oswald', 'sans-serif'],
        }
    },
  },
  plugins: [],
}

