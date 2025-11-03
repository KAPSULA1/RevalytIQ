import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ProfilePage from "../app/profile/page";
import { updateProfile, logout } from "../lib/auth";
import { useAuth } from "../lib/store";

const replaceMock = jest.fn();

jest.mock("next/navigation", () => ({
  useRouter: () => ({ replace: replaceMock }),
}));

jest.mock("../lib/auth", () => {
  const actual = jest.requireActual("../lib/auth");
  return {
    ...actual,
    updateProfile: jest.fn().mockResolvedValue({ id: 9, username: "updated", email: "updated@example.com" }),
    logout: jest.fn().mockResolvedValue(undefined),
  };
});

jest.mock("react-hot-toast", () => ({ success: jest.fn(), error: jest.fn() }));

describe("ProfilePage", () => {
  beforeEach(() => {
    replaceMock.mockClear();
    (updateProfile as jest.Mock).mockClear();
    (logout as jest.Mock).mockClear();
    act(() => {
      useAuth.setState({ user: { id: 9, username: "profile", email: "profile@example.com" }, initialized: true });
    });
  });

  it("allows updating profile fields", async () => {
    render(<ProfilePage />);

    const usernameInput = screen.getByDisplayValue("profile") as HTMLInputElement;
    const emailInput = screen.getByDisplayValue("profile@example.com") as HTMLInputElement;

    await act(async () => {
      await userEvent.clear(usernameInput);
      await userEvent.type(usernameInput, "updated");
      await userEvent.clear(emailInput);
      await userEvent.type(emailInput, "updated@example.com");
    });

    fireEvent.click(screen.getByText(/Save/i));

    await waitFor(() => {
      expect(updateProfile).toHaveBeenCalledTimes(1);
      expect(useAuth.getState().user?.username).toBe("updated");
    });

    fireEvent.click(screen.getByText(/Logout/i));
    await waitFor(() => {
      expect(logout).toHaveBeenCalled();
      expect(replaceMock).toHaveBeenCalledWith("/");
      expect(useAuth.getState().user).toBeNull();
    });
  });
});
