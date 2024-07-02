module.exports = {
    content: ["./pages/**/*.tsx", "./src/**/*.tsx"],
    theme: {
        extend: {
            colors: {
                "theme-secondary": "#258eb2",
                "theme-tertiary": "#f8f8f8",
                "theme-gray": "#bcc2c4",
            },
            transitionProperty: {
                "max-height": "max-height",
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [require("@tailwindcss/typography")],
};
