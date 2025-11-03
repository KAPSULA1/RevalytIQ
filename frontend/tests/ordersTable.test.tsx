import { render, screen } from "@testing-library/react";
import OrdersTable from "../app/dashboard/components/OrdersTable";
import type { Order } from "../lib/auth";

describe("OrdersTable", () => {
  it("formats order rows", () => {
    const orders: Order[] = [
      {
        id: 1,
        customer: "Alice",
        amount: 123.456,
        status: "paid",
        created_at: new Date("2024-01-01T00:00:00Z").toISOString(),
      },
    ];

    render(<OrdersTable orders={orders} />);

    expect(screen.getByText("$123.46")).toBeInTheDocument();
    expect(screen.getByText(/paid/i)).toHaveClass("text-emerald-600");
  });
});
