"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import api from "@/lib/api/client";

interface PublicOrderResponse {
  public_uid: string;
  device_name: string;
  device_address: string | null;
  created_at: string;
  expires_at: string;
  code_masked: string;
  qr_svg: string;
  map_point: { lat: number; lon: number };
}

export default function PublicOrderPage() {
  const params = useParams<{ publicUid: string }>();
  const [remaining, setRemaining] = useState<string>("--:--:--");
  const { data } = useQuery<PublicOrderResponse>({
    queryKey: ["public-order", params.publicUid],
    queryFn: async () => (await api.get(`/public/orders/${params.publicUid}`)).data
  });

  useEffect(() => {
    if (!data) return;
    const interval = setInterval(() => {
      const diff = new Date(data.expires_at).getTime() - Date.now();
      const totalSeconds = Math.max(Math.floor(diff / 1000), 0);
      const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
      const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
      const seconds = String(totalSeconds % 60).padStart(2, "0");
      setRemaining(`${hours}:${minutes}:${seconds}`);
    }, 1000);
    return () => clearInterval(interval);
  }, [data]);

  return (
    <main className="flex min-h-screen flex-col gap-6 bg-slate-900 px-6 py-10 text-white">
      <div className="mx-auto w-full max-w-lg rounded-3xl bg-white p-6 text-slate-900 shadow-2xl">
        <h1 className="text-2xl font-semibold">Получение заказа</h1>
        <p className="mt-1 text-sm text-muted">Заказ #{data?.public_uid}</p>
        <div className="mt-4 space-y-3">
          <div className="rounded-2xl bg-slate-100 p-4">
            <span className="text-sm text-muted">Код доступа</span>
            <p className="mt-2 text-4xl font-bold tracking-widest">{data?.code_masked ?? "••••"}</p>
            <p className="mt-2 text-sm text-muted">Срок хранения истечёт через {remaining}</p>
          </div>
          <div className="rounded-2xl bg-slate-100 p-4">
            <span className="text-sm text-muted">QR для сканирования</span>
            <div className="mt-2 flex h-40 items-center justify-center rounded-xl bg-white">
              <span className="text-muted">{data?.qr_svg ?? "QR"}</span>
            </div>
          </div>
          <div className="rounded-2xl bg-slate-100 p-4">
            <span className="text-sm text-muted">Постамат</span>
            <p className="mt-1 text-base font-semibold">{data?.device_name}</p>
            <p className="text-sm text-muted">{data?.device_address ?? "Адрес уточняется"}</p>
            <div className="mt-3 h-40 w-full rounded-xl bg-slate-200" />
          </div>
          <button className="w-full rounded-full border border-primary py-3 text-primary">Сообщить о проблеме</button>
        </div>
      </div>
    </main>
  );
}
