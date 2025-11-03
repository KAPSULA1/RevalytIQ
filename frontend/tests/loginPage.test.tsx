import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import LoginPage from "../app/page";
import { login, me } from "../lib/auth";
import { useAuth } from "../lib/store";

const pushMock = jest.fn();
const replaceMock = jest.fn();

jest.mock("next/navigation", () => ({
  useRouter: () => ({ push: pushMock, replace: replaceMock }),
}));

jest.mock("../lib/auth", () => {
  const actual = jest.requireActual("../lib/auth");
  return {
    ...actual,
    login: jest.fn().mockResolvedValue({ detail: "ok" }),
    me: jest.fn().mockResolvedValue({ id: 42, username: "demo", email: "demo@example.com" }),
  };
});

jest.mock("react-hot-toast", () => ({ success: jest.fn() }));

describe("LoginPage", () => {
  beforeEach(() => {
    pushMock.mockClear();
    replaceMock.mockClear();
    (login as jest.Mock).mockClear();
    (me as jest.Mock).mockClear();
    act(() => {
      useAuth.setState({ user: null, initialized: false });
    });
  });

  it("shows validation error when credentials missing", () => {
    render(<LoginPage />);
    fireEvent.click(screen.getByText(/Sign In/i));
    expect(screen.getByText(/please enter both username and password/i)).toBeInTheDocument();
    expect(login).not.toHaveBeenCalled();
  });

  it("logs in and redirects to dashboard", async () => {
    render(<LoginPage />);

    fireEvent.change(screen.getByPlaceholderText(/Username/i), {
      target: { value: "demo" },
    });
    fireEvent.change(screen.getByPlaceholderText(/Password/i), {
      target: { value: "s3cret" },
    });

    fireEvent.submit(screen.getByRole("button", { name: /Sign In/i }));

    await waitFor(() => {
      expect(login).toHaveBeenCalledWith("demo", "s3cret");
      expect(me).toHaveBeenCalled();
      expect(pushMock).toHaveBeenCalledWith("/dashboard");
      expect(useAuth.getState().user?.username).toEqual("demo");
    });
  });
});
