"use client";

import { useQuery } from "@tanstack/react-query";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis, BarChart, Bar } from "recharts";
import api from "@/lib/api/client";

interface AnalyticsResponse {
  occupancy_series: { date: string; occupancy_percent: number }[];
  romi: { channel: string; spend: number; revenue: number }[];
}

export function AnalyticsCharts() {
  const { data } = useQuery<AnalyticsResponse>({
    queryKey: ["analytics", "series"],
    queryFn: async () => (await api.get("/analytics/dashboard")).data
  });

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Заполненность</h2>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={data?.occupancy_series ?? []}>
            <defs>
              <linearGradient id="colorOccupancy" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#2563eb" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="date" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Area type="monotone" dataKey="occupancy_percent" stroke="#2563eb" fill="url(#colorOccupancy)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">ROMI по каналам</h2>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={data?.romi ?? []}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="channel" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="revenue" fill="#22c55e" name="Доход" />
            <Bar dataKey="spend" fill="#ef4444" name="Затраты" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
