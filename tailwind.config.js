/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    './templates/**/*.html', // Include all HTML templates
    './static/js/**/*.js',   // Include JavaScript files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
