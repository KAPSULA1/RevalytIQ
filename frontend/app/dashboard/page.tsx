"use client";
import { useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import Navbar from "../../components/Navbar";
import Sidebar from "../../components/Sidebar";
import KPIStat from "./components/KPIStat";
import RevenueChart from "./components/RevenueChart";
import OrdersTable from "./components/OrdersTable";
import { fetchKPIs, fetchOrders, Order } from "../../lib/auth";
import { useAuth } from "../../lib/store";

export default function Dashboard() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const user = useAuth((s) => s.user);
  const initialized = useAuth((s) => s.initialized);

  // 🔐 Authentication check
  useEffect(() => {
    if (!initialized) return;
    if (!user) {
      router.replace("/");
    }
  }, [initialized, user, router]);

  // 📊 Fetch KPIs and Orders
  const kpiQ = useQuery({
    queryKey: ["kpis"],
    queryFn: fetchKPIs,
    enabled: initialized && !!user,
  });
  const ordersQ = useQuery({
    queryKey: ["orders"],
    queryFn: fetchOrders,
    enabled: initialized && !!user,
  });

  // 💰 Aggregate revenue over time
  const revenueSeries = useMemo(() => {
    const items = (Array.isArray(ordersQ.data)
      ? ordersQ.data
      : ordersQ.data?.results) as Order[] | undefined;
    const buckets = new Map<string, number>();
    (items ?? []).forEach((o) => {
      const d = new Date(o.created_at);
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
        d.getDate()
      ).padStart(2, "0")}`;
      const numericAmount = Number.parseFloat(String(o.amount ?? 0));
      if (!Number.isFinite(numericAmount)) return;
      buckets.set(key, (buckets.get(key) ?? 0) + numericAmount);
    });
    return Array.from(buckets.entries()).map(([x, y]) => {
      const numericY = Number.parseFloat(String(y));
      return {
        x,
        y: Number.isFinite(numericY) ? Number(numericY.toFixed(2)) : 0,
      };
    });
  }, [ordersQ.data]);

  // 🔄 Refresh handler
  const onRefresh = async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ["kpis"] }),
      queryClient.invalidateQueries({ queryKey: ["orders"] }),
    ]);
    toast.success("Data refreshed");
  };

  // 🌀 Loading / Error states
  const anyLoading = kpiQ.isLoading || ordersQ.isLoading;
  const anyError = kpiQ.isError || ordersQ.isError;

  if (!initialized || anyLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen text-gray-500">
        Loading analytics data...
      </div>
    );
  }

  return (
    <div className="min-h-screen grid grid-rows-[auto_1fr] bg-gray-50">
      <Navbar />
      <div className="grid grid-cols-[240px_1fr]">
        <Sidebar />
        <main className="p-6 space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold">Analytics Overview</h1>
            <button
              onClick={onRefresh}
              className="text-sm px-3 py-1.5 rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60"
              disabled={anyLoading}
            >
              {anyLoading ? "Refreshing..." : "Refresh"}
            </button>
          </div>

          {anyError && (
            <p className="text-red-600">Failed to load data. Please refresh.</p>
          )}

          <div className="grid md:grid-cols-3 gap-4">
            <KPIStat
              label="Revenue"
              value={kpiQ.data ? `$${kpiQ.data.revenue.toFixed(2)}` : "..."}
            />
            <KPIStat label="Orders" value={kpiQ.data?.orders ?? "..."} />
            <KPIStat label="AOV" value={kpiQ.data ? `$${kpiQ.data.aov}` : "..."} />
          </div>

          <RevenueChart points={revenueSeries} />

          <div>
            <h2 className="text-lg font-semibold mb-3">Recent Orders</h2>
            <OrdersTable
              orders={
                (Array.isArray(ordersQ.data)
                  ? ordersQ.data
                  : ordersQ.data?.results) ?? []
              }
            />
          </div>
        </main>
      </div>
    </div>
  );
}
