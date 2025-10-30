"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api/client";

interface Cell {
  id: number;
  code: string;
  status: string;
  cooled: boolean;
  needs_repair: boolean;
  open: boolean;
}

interface Device {
  id: number;
  name: string;
  code: string;
  status_online: boolean;
  cells: Cell[];
}

export function DeviceGrid() {
  const { data } = useQuery<Device[]>({
    queryKey: ["devices"],
    queryFn: async () => (await api.get("/devices")).data
  });

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {data?.map((device) => (
        <div key={device.id} className="card">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">{device.name}</h2>
              <p className="text-sm text-muted">{device.code}</p>
            </div>
            <span
              className={`badge ${device.status_online ? "bg-green-100 text-green-700" : "bg-red-100 text-red-600"}`}
            >
              {device.status_online ? "online" : "offline"}
            </span>
          </div>
          <div className="mt-4 grid grid-cols-6 gap-2">
            {device.cells.slice(0, 12).map((cell) => (
              <div
                key={cell.id}
                className={`flex h-12 items-center justify-center rounded-md text-xs font-medium ${
                  cell.status === "occupied"
                    ? "bg-blue-500/20 text-blue-700"
                    : cell.status === "fault"
                    ? "bg-red-500/20 text-red-600"
                    : cell.needs_repair
                    ? "bg-amber-200 text-amber-700"
                    : "bg-slate-200 text-slate-700"
                }`}
              >
                {cell.code}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
