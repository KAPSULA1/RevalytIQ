import { render, screen } from "@testing-library/react";
import RevenueChart from "../app/dashboard/components/RevenueChart";

jest.mock("react-chartjs-2", () => ({
  Line: ({ data }: { data: unknown }) => (
    <div data-testid="mock-chart" data-payload={JSON.stringify(data)} />
  ),
}));

describe("RevenueChart", () => {
  it("maps points into chart dataset", () => {
    const points = [
      { x: "2024-01-01", y: 10 },
      { x: "2024-01-02", y: 20 },
    ];

    render(<RevenueChart points={points} />);

    const chart = screen.getByTestId("mock-chart");
    const payload = JSON.parse(chart.getAttribute("data-payload") ?? "{}");
    expect(payload.labels).toEqual(["2024-01-01", "2024-01-02"]);
    expect(payload.datasets[0].data).toEqual([10, 20]);
  });
});
