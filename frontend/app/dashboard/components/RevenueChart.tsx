"use client";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend } from "chart.js";
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend);

export default function RevenueChart({ points }: { points: { x: string; y: number }[] }) {
  const data = {
    labels: points.map(p => p.x),
    datasets: [{ label: "Revenue", data: points.map(p => p.y) }]
  };
  const options = { responsive: true, maintainAspectRatio: false } as const;
  return <div className="h-64 bg-white rounded-xl p-4 shadow border"><Line data={data} options={options} /></div>;
}
