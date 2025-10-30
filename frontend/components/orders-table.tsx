"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api/client";
import dayjs from "dayjs";

interface OrderRow {
  id: number;
  public_uid: string;
  device_id: number;
  cell_id: number | null;
  type: string;
  status: string;
  created_at: string;
  expires_at: string | null;
  access_code?: { code_masked: string; qr_token: string } | null;
  payload?: Record<string, unknown> | null;
}

export function OrdersTable() {
  const { data } = useQuery<OrderRow[]>({
    queryKey: ["orders"],
    queryFn: async () => (await api.get("/orders")).data
  });

  return (
    <div className="card overflow-x-auto">
      <table className="min-w-full text-left">
        <thead>
          <tr className="text-xs uppercase text-muted">
            <th className="px-4 py-2">№</th>
            <th className="px-4 py-2">Устройство</th>
            <th className="px-4 py-2">Статус</th>
            <th className="px-4 py-2">Тип</th>
            <th className="px-4 py-2">Создан</th>
            <th className="px-4 py-2">Срок</th>
            <th className="px-4 py-2">Код</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
          {data?.map((order) => (
            <tr key={order.id} className="text-sm">
              <td className="px-4 py-3 font-medium">{order.public_uid}</td>
              <td className="px-4 py-3">#{order.device_id}</td>
              <td className="px-4 py-3">
                <span className="badge bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-100">
                  {order.status}
                </span>
              </td>
              <td className="px-4 py-3">{order.type}</td>
              <td className="px-4 py-3">{dayjs(order.created_at).format("DD.MM.YYYY HH:mm")}</td>
              <td className="px-4 py-3">{order.expires_at ? dayjs(order.expires_at).format("DD.MM HH:mm") : "—"}</td>
              <td className="px-4 py-3">{order.access_code?.code_masked ?? "***"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
