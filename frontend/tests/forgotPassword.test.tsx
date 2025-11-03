import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ForgotPasswordPage from "../app/forgot-password/page";
import { forgotPassword } from "../lib/auth";

jest.mock("../lib/auth", () => {
  const actual = jest.requireActual("../lib/auth");
  return {
    ...actual,
    forgotPassword: jest.fn().mockResolvedValue({
      detail: "Check your inbox.",
      token: "demo-reset-token",
      uid: "demo-uid",
    }),
  };
});

describe("ForgotPasswordPage", () => {
  it("submits email and displays demo token in debug mode", async () => {
    render(<ForgotPasswordPage />);

    fireEvent.change(screen.getByPlaceholderText(/Email/i), {
      target: { value: "user@example.com" },
    });
    fireEvent.click(screen.getByText(/Send reset link/i));

    await waitFor(() => {
      expect(forgotPassword).toHaveBeenCalledWith("user@example.com");
    });

    expect(screen.getByText(/Check your inbox/i)).toBeInTheDocument();
    expect(screen.getByText(/demo-reset-token/i)).toBeInTheDocument();
  });
});
