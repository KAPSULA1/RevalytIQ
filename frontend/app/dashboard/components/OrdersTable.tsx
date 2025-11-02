"use client";
import type { Order } from "../../../lib/auth";

export default function OrdersTable({ orders }: { orders: Order[] }) {
  return (
    <div className="bg-white rounded-xl p-4 shadow border overflow-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left border-b">
            <th className="py-2">ID</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((o) => {
            const amountValue = Number.parseFloat(String(o.amount ?? 0));
            const displayAmount = Number.isFinite(amountValue) ? amountValue.toFixed(2) : "0.00";

            return (
              <tr key={o.id} className="border-b last:border-0">
                <td className="py-2">{o.id}</td>
                <td>${displayAmount}</td>
                <td className={o.status === "paid" ? "text-emerald-600" : "text-rose-600"}>
                  {o.status}
                </td>
                <td>{new Date(o.created_at).toLocaleString()}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
