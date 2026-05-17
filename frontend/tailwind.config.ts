import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        forest: {
          50: "#eef8f1",
          100: "#d9efe1",
          500: "#237a45",
          600: "#176538",
          700: "#11512d",
          800: "#0c4023",
        },
      },
      boxShadow: {
        soft: "0 18px 45px rgba(15, 61, 35, 0.10)",
      },
    },
  },
  plugins: [],
};

export default config;

