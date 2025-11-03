import { fireEvent, render, screen } from "@testing-library/react";
import Dashboard from "../app/dashboard/page";
import { useAuth } from "../lib/store";

const replaceMock = jest.fn();
const invalidateQueriesMock = jest.fn();
const successToast = jest.fn();

const useQueryMock = jest.fn((queryKey) => ({ data: undefined, isLoading: false, isError: false }));

jest.mock("next/navigation", () => ({
  useRouter: () => ({ replace: replaceMock }),
}));

jest.mock("@tanstack/react-query", () => ({
  useQuery: (options: any) => useQueryMock(options),
  useQueryClient: () => ({ invalidateQueries: invalidateQueriesMock }),
}));

jest.mock("react-hot-toast", () => ({ success: (msg: string) => successToast(msg) }));

jest.mock("../components/Navbar", () => () => <div data-testid="navbar" />);
jest.mock("../components/Sidebar", () => () => <div data-testid="sidebar" />);
jest.mock("../app/dashboard/components/KPIStat", () => ({ label, value }: { label: string; value: string }) => (
  <div data-testid={`kpi-${label}`}>{value}</div>
));
jest.mock("../app/dashboard/components/RevenueChart", () => () => <div data-testid="chart" />);
jest.mock("../app/dashboard/components/OrdersTable", () => () => <div data-testid="orders-table" />);

const resetAuthStore = () => {
  useAuth.setState({ user: null, initialized: false });
  replaceMock.mockClear();
  invalidateQueriesMock.mockClear();
  successToast.mockClear();
  useQueryMock.mockImplementation(() => ({ data: undefined, isLoading: false, isError: false }));
};

describe("Dashboard page", () => {
  beforeEach(() => {
    resetAuthStore();
  });

  it("redirects to login when unauthenticated", () => {
    useAuth.setState({ user: null, initialized: true });
    render(<Dashboard />);
    expect(replaceMock).toHaveBeenCalledWith("/");
  });

  it("renders analytics when user is present", () => {
    useAuth.setState({
      user: { id: 1, username: "demo", email: "demo@example.com" },
      initialized: true,
    });
    useQueryMock.mockImplementation(({ queryKey }) => {
      if (queryKey[0] === "kpis") {
        return { data: { revenue: 100, orders: 5, aov: 20 }, isLoading: false, isError: false };
      }
      return { data: [{ id: 1, created_at: new Date().toISOString(), amount: 50, status: "paid" }], isLoading: false, isError: false };
    });

    render(<Dashboard />);
    expect(screen.getByTestId("navbar")).toBeInTheDocument();
    expect(screen.getByTestId("kpi-Revenue")).toHaveTextContent("$100.00");
  });

  it("shows loading state while queries resolve", () => {
    useAuth.setState({ user: { id: 1, username: "demo", email: "demo@example.com" }, initialized: true });
    useQueryMock.mockReturnValue({ data: undefined, isLoading: true, isError: false });

    render(<Dashboard />);
    expect(screen.getByText(/Loading analytics data/i)).toBeInTheDocument();
  });

  it("displays error message and refresh triggers invalidation", async () => {
    useAuth.setState({ user: { id: 1, username: "demo", email: "demo@example.com" }, initialized: true });
    useQueryMock.mockImplementation(({ queryKey }) => ({
      data: queryKey[0] === "kpis" ? { revenue: 0, orders: 0, aov: 0 } : [],
      isLoading: false,
      isError: true,
    }));

    render(<Dashboard />);
    expect(screen.getByText(/Failed to load data/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /Refresh/i }));
    expect(invalidateQueriesMock).toHaveBeenCalledTimes(2);
    await screen.findByText(/Failed to load data/i); // ensure render cycle completes
    expect(successToast).toHaveBeenCalledWith("Data refreshed");
  });
});
