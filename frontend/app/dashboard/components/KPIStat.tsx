type KPIStatProps = { label: string; value: number | string };
export default function KPIStat({ label, value }: KPIStatProps) {
  return (
    <div className="bg-white rounded-xl p-4 shadow border">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-2xl font-semibold mt-1">{value}</div>
    </div>
  );
}
