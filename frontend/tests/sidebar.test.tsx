import { render, screen } from "@testing-library/react";
import Sidebar from "../components/Sidebar";

const usePathname = jest.fn();

jest.mock("next/navigation", () => ({
  usePathname: () => usePathname(),
}));

describe("Sidebar", () => {
  it("highlights the active link", () => {
    usePathname.mockReturnValue("/dashboard");
    render(<Sidebar />);

    const dashboardLink = screen.getByText(/Dashboard/i);
    expect(dashboardLink).toHaveClass("bg-blue-50");

    const profileLink = screen.getByText(/Profile/i);
    expect(profileLink).not.toHaveClass("bg-blue-50");
  });
});
