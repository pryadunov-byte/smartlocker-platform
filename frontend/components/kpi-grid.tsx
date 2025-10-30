"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api/client";

interface KpiResponse {
  devices_online: number;
  devices_offline: number;
  active_orders: number;
  overdue_orders: number;
  average_storage_time_hours: number;
}

export function KpiGrid() {
  const { data } = useQuery<KpiResponse>({
    queryKey: ["analytics", "dashboard"],
    queryFn: async () => {
      const response = await api.get("/analytics/dashboard");
      return response.data;
    }
  });

  const kpis = [
    { label: "Активные устройства", value: data?.devices_online ?? 0 },
    { label: "Оффлайн устройства", value: data?.devices_offline ?? 0 },
    { label: "Активные заказы", value: data?.active_orders ?? 0 },
    { label: "Просрочки", value: data?.overdue_orders ?? 0 },
    { label: "Среднее время хранения", value: `${data?.average_storage_time_hours ?? 0} ч` }
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {kpis.map((item) => (
        <div key={item.label} className="card">
          <span className="text-sm text-muted">{item.label}</span>
          <p className="mt-2 text-3xl font-semibold">{item.value}</p>
        </div>
      ))}
    </div>
  );
}
