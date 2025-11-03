/** @type {import('jest').Config} */
module.exports = {
  preset: "ts-jest",
  testEnvironment: "jsdom",

  // Ensure Jest finds tests in common folders
  testMatch: [
    "<rootDir>/tests/**/*.(spec|test).[jt]s?(x)",
    "<rootDir>/app/**/*.(spec|test).[jt]s?(x)",
    "<rootDir>/components/**/*.(spec|test).[jt]s?(x)",
    "<rootDir>/lib/**/*.(spec|test).[jt]s?(x)",
  ],

  transform: {
    "^.+\\.(ts|tsx)$": "ts-jest",
  },

  setupFilesAfterEnv: ["<rootDir>/tests/setup.ts"],

  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/$1",
  },

  testPathIgnorePatterns: [
    "<rootDir>/.next/",
    "<rootDir>/node_modules/",
  ],

  collectCoverageFrom: [
    "app/**/*.{ts,tsx}",
    "components/**/*.{ts,tsx}",
    "lib/**/*.{ts,tsx}",
    "tests/**/*.{ts,tsx}",
    "!app/layout.tsx",
    "!lib/api.ts",
  ],

  coverageThreshold: {
    global: {
      statements: 70,
      branches: 70,
      functions: 70,
      lines: 70,
    },
  },
};
