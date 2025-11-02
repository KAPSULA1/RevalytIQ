import { render, screen } from "@testing-library/react";
import KPIStat from "../app/dashboard/components/KPIStat";

test("renders KPI label and value correctly", () => {
  render(<KPIStat label="Revenue" value="$999.99" />);
  expect(screen.getByText("Revenue")).toBeInTheDocument();
  expect(screen.getByText("$999.99")).toBeInTheDocument();
});
