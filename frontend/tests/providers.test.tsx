import { render, screen, waitFor } from "@testing-library/react";
import Providers from "../lib/Providers";
import { me } from "../lib/auth";
import { useAuth } from "../lib/store";

jest.mock("../lib/auth", () => {
  const actual = jest.requireActual("../lib/auth");
  return {
    ...actual,
    me: jest.fn().mockResolvedValue({ id: 7, username: "loaded", email: "loaded@example.com" }),
  };
});

describe("Providers", () => {
  it("hydrates user state from API", async () => {
    render(
      <Providers>
        <div>child</div>
      </Providers>
    );

    expect(screen.getByText(/child/i)).toBeInTheDocument();
    await waitFor(() => {
      expect(me).toHaveBeenCalled();
      expect(useAuth.getState().user?.username).toBe("loaded");
      expect(useAuth.getState().initialized).toBe(true);
    });
  });
});
