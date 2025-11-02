import { api } from "../lib/api";

test("axios instance has a baseURL", () => {
  expect(api.defaults.baseURL).toContain("http");
});
