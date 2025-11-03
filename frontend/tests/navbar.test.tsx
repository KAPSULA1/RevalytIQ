import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import Navbar from "../components/Navbar";
import { useAuth } from "../lib/store";
import { logout as logoutApi } from "../lib/auth";

const replaceMock = jest.fn();

jest.mock("next/navigation", () => ({
  useRouter: () => ({ replace: replaceMock }),
}));

jest.mock("../lib/auth", () => {
  const actual = jest.requireActual("../lib/auth");
  return {
    ...actual,
    logout: jest.fn().mockResolvedValue(undefined),
  };
});

jest.mock("react-hot-toast", () => ({
  success: jest.fn(),
}));

describe("Navbar", () => {
  beforeEach(() => {
    replaceMock.mockClear();
    (logoutApi as jest.Mock).mockClear();
  });

  it("renders profile link and handles logout", async () => {
    act(() => {
      useAuth.setState({
        user: { id: 1, username: "demo", email: "demo@example.com" },
        initialized: true,
      });
    });

    render(<Navbar />);

    expect(screen.getByText(/Profile/i)).toBeInTheDocument();
    fireEvent.click(screen.getByText(/Logout/i));

    await waitFor(() => {
      expect(logoutApi).toHaveBeenCalledTimes(1);
      expect(replaceMock).toHaveBeenCalledWith("/");
    });
    expect(useAuth.getState().user).toBeNull();
  });
});
