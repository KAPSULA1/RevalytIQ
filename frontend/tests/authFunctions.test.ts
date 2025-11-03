import { api } from "../lib/api";

jest.mock("../lib/api", () => {
  const post = jest.fn();
  const get = jest.fn();
  const patch = jest.fn();
  return {
    api: {
      post,
      get,
      patch,
      defaults: { baseURL: "http://test" },
      interceptors: { response: { use: jest.fn() } },
    },
  };
});

const mockedApi = api as unknown as {
  post: jest.Mock;
  get: jest.Mock;
  patch: jest.Mock;
};

const { login, register, forgotPassword, resetPassword, me, updateProfile, logout, fetchOrders, fetchKPIs } =
  require("../lib/auth");

describe("auth API helpers", () => {
  beforeEach(() => {
    mockedApi.post.mockReset();
    mockedApi.get.mockReset();
    mockedApi.patch.mockReset();
  });

  it("calls login endpoint", async () => {
    mockedApi.post.mockResolvedValueOnce({ data: { detail: "ok" } });
    await expect(login("demo", "secret" )).resolves.toEqual({ detail: "ok" });
    expect(mockedApi.post).toHaveBeenCalledWith("/api/auth/token/", { username: "demo", password: "secret" });
  });

  it("registers a user", async () => {
    const response = { id: 1, username: "demo", email: "demo@example.com" };
    mockedApi.post.mockResolvedValueOnce({ data: response });
    await expect(register("demo", "demo@example.com", "pw", "pw")).resolves.toEqual(response);
    expect(mockedApi.post).toHaveBeenCalledWith("/api/auth/register/", {
      username: "demo",
      email: "demo@example.com",
      password: "pw",
      password2: "pw",
    });
  });

  it("requests password reset flow", async () => {
    mockedApi.post.mockResolvedValueOnce({ data: { detail: "ok", token: "t", uid: "u" } });
    await expect(forgotPassword("demo@example.com")).resolves.toEqual({ detail: "ok", token: "t", uid: "u" });
    expect(mockedApi.post).toHaveBeenCalledWith("/api/auth/password/forgot/", { email: "demo@example.com" });

    mockedApi.post.mockResolvedValueOnce({ data: { detail: "done" } });
    await resetPassword({ email: "demo@example.com", uid: "u", token: "t", new_password: "new", new_password2: "new" });
    expect(mockedApi.post).toHaveBeenLastCalledWith("/api/auth/password/reset/", {
      email: "demo@example.com",
      uid: "u",
      token: "t",
      new_password: "new",
      new_password2: "new",
    });
  });

  it("fetches profile and updates it", async () => {
    mockedApi.get.mockResolvedValueOnce({ data: { id: 1, username: "demo", email: "demo@example.com" } });
    await me();
    expect(mockedApi.get).toHaveBeenCalledWith("/api/auth/me/");

    mockedApi.patch.mockResolvedValueOnce({ data: { id: 1, username: "new", email: "new@example.com" } });
    await updateProfile({ username: "new" });
    expect(mockedApi.patch).toHaveBeenCalledWith("/api/auth/profile/", { username: "new" });
  });

  it("logs out and fetches analytics", async () => {
    mockedApi.post.mockResolvedValueOnce({ data: {} });
    await logout();
    expect(mockedApi.post).toHaveBeenCalledWith("/api/auth/logout/");

    mockedApi.get.mockResolvedValueOnce({ data: [{ id: 1 }] });
    await fetchOrders();
    expect(mockedApi.get).toHaveBeenCalledWith("/api/analytics/orders/");

    mockedApi.get.mockResolvedValueOnce({ data: { revenue: 0, orders: 0, aov: 0 } });
    await fetchKPIs();
    expect(mockedApi.get).toHaveBeenCalledWith("/api/analytics/kpis/");
  });
});
