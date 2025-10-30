"use client";

import { useState } from "react";

const modes = ["Получение", "Возврат", "Аренда", "Хранение"];

export default function DeviceSimulatorPage() {
  const [pin, setPin] = useState("");
  const [step, setStep] = useState<"pin" | "open" | "payment">("pin");

  return (
    <main className="flex min-h-screen flex-col items-center bg-slate-900 px-6 py-12 text-white">
      <div className="w-full max-w-md rounded-3xl bg-black/60 p-6 shadow-2xl">
        <h1 className="text-center text-2xl font-semibold uppercase tracking-wide">Эмулятор устройства</h1>
        <div className="mt-4 flex justify-center gap-2 text-xs uppercase text-slate-400">
          {modes.map((mode) => (
            <span key={mode} className="rounded-full bg-white/10 px-3 py-1">
              {mode}
            </span>
          ))}
        </div>
        {step === "pin" && (
          <div className="mt-6 space-y-4">
            <p className="text-center text-sm text-slate-300">Введите PIN-код, полученный в SMS</p>
            <div className="flex justify-center gap-2">
              {Array.from({ length: 4 }).map((_, idx) => (
                <span key={idx} className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/10 text-2xl">
                  {pin[idx] ?? "•"}
                </span>
              ))}
            </div>
            <div className="grid grid-cols-3 gap-3">
              {Array.from({ length: 9 }, (_, idx) => idx + 1).map((digit) => (
                <button
                  key={digit}
                  className="rounded-xl bg-primary py-4 text-xl"
                  onClick={() => setPin((prev) => (prev + digit.toString()).slice(0, 4))}
                >
                  {digit}
                </button>
              ))}
              <button className="rounded-xl bg-slate-700 py-4 text-xl" onClick={() => setPin("")}>Стереть</button>
              <button className="rounded-xl bg-primary py-4 text-xl" onClick={() => setStep("payment")}>0</button>
              <button className="rounded-xl bg-green-500 py-4 text-xl" onClick={() => setStep("open")}>ОК</button>
            </div>
          </div>
        )}
        {step === "payment" && (
          <div className="mt-6 space-y-4 text-center">
            <h2 className="text-xl font-semibold">Требуется предоплата</h2>
            <p className="text-sm text-slate-300">Оплата услуги: 150 ₽</p>
            <button className="w-full rounded-full bg-primary py-3" onClick={() => setStep("open")}>
              Оплатить и продолжить
            </button>
          </div>
        )}
        {step === "open" && (
          <div className="mt-6 space-y-4 text-center">
            <h2 className="text-xl font-semibold">Ячейки открыты</h2>
            <p className="text-sm text-slate-300">A1, B3</p>
            <div className="flex flex-col gap-3">
              <button className="w-full rounded-full bg-green-500 py-3">Я забрал заказ</button>
              <button className="w-full rounded-full bg-amber-500 py-3">Проблема</button>
              <span className="text-xs text-slate-500">Телефон техподдержки: +7 800 555-35-35</span>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
