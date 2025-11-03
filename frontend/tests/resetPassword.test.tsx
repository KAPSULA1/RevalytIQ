import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ResetPasswordPage from "../app/reset-password/page";
import { resetPassword } from "../lib/auth";

jest.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams("email=user@example.com&uid=demo-uid&token=demo-token"),
}));

jest.mock("../lib/auth", () => {
  const actual = jest.requireActual("../lib/auth");
  return {
    ...actual,
    resetPassword: jest.fn().mockResolvedValue({ detail: "Password successfully reset." }),
  };
});

describe("ResetPasswordPage", () => {
  it("submits new password", async () => {
    render(<ResetPasswordPage />);

    fireEvent.change(screen.getByPlaceholderText(/New password/i), {
      target: { value: "NewPass123" },
    });
    fireEvent.change(screen.getByPlaceholderText(/Confirm password/i), {
      target: { value: "NewPass123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /Reset password/i }));

    await waitFor(() => {
      expect(resetPassword).toHaveBeenCalledWith({
        email: "user@example.com",
        uid: "demo-uid",
        token: "demo-token",
        new_password: "NewPass123",
        new_password2: "NewPass123",
      });
    });

    expect(screen.getByText(/Password successfully reset/i)).toBeInTheDocument();
  });
});
