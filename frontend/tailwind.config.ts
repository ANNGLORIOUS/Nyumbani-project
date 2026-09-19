import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: { extend: { colors: { forest: '#14532D', gold: '#D4A72C', ink: '#17201A', canvas: '#F8FAF8' }, boxShadow: { card: '0 10px 30px rgba(20, 83, 45, .08)' } } },
  plugins: [],
} satisfies Config
