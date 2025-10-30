"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function PublicEntryPage() {
  const router = useRouter();
  const [code, setCode] = useState("");

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-slate-900 px-6 text-white">
      <div className="w-full max-w-sm rounded-3xl bg-black/50 p-6">
        <h1 className="text-center text-2xl font-semibold">Введите код заказа</h1>
        <p className="mt-2 text-center text-sm text-slate-400">Используйте код из SMS или e-mail</p>
        <div className="mt-6 grid grid-cols-3 gap-3 text-xl">
          {Array.from({ length: 9 }, (_, idx) => idx + 1).map((digit) => (
            <button
              key={digit}
              className="rounded-xl bg-primary py-4"
              onClick={() => setCode((prev) => (prev + digit.toString()).slice(0, 6))}
            >
              {digit}
            </button>
          ))}
          <button className="rounded-xl bg-slate-700 py-4" onClick={() => setCode("")}>Стереть</button>
          <button className="rounded-xl bg-primary py-4" onClick={() => setCode((prev) => (prev + "0").slice(0, 6))}>0</button>
          <button
            className="rounded-xl bg-green-500 py-4"
            onClick={() => code && router.push(`/public/${code}`)}
          >
            Открыть
          </button>
        </div>
        <div className="mt-6 flex justify-center gap-2 text-2xl tracking-widest">
          {Array.from({ length: 6 }).map((_, idx) => (
            <span key={idx}>{code[idx] ?? "•"}</span>
          ))}
        </div>
      </div>
    </main>
  );
}
