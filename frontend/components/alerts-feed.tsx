"use client";

import { useEffect } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api/client";

interface AlertItem {
  id: number;
  device_id: number;
  severity: string;
  kind: string;
  message: string | null;
  created_at: string;
}

export function AlertsFeed() {
  const queryClient = useQueryClient();
  const { data } = useQuery<AlertItem[]>({
    queryKey: ["alerts"],
    queryFn: async () => (await api.get("/alerts")).data
  });

  useEffect(() => {
    const id = setInterval(() => {
      queryClient.invalidateQueries({ queryKey: ["alerts"], exact: true });
    }, 15000);
    return () => clearInterval(id);
  }, [queryClient]);

  return (
    <div className="card">
      <h2 className="text-lg font-semibold mb-4">Лента алертов</h2>
      <ul className="space-y-3">
        {data?.map((alert) => (
          <li key={alert.id} className="rounded-lg border border-slate-200 p-3 dark:border-slate-700">
            <div className="flex items-center justify-between text-sm">
              <span className="font-medium">Устройство #{alert.device_id}</span>
              <span className="badge bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-200">
                {alert.severity}
              </span>
            </div>
            <p className="mt-1 text-sm text-muted">{alert.kind}</p>
            {alert.message && <p className="mt-2 text-sm">{alert.message}</p>}
          </li>
        ))}
      </ul>
    </div>
  );
}
