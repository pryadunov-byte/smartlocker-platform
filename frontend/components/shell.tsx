"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

const navItems = [
  { href: "/admin/dashboard", label: "Дашборд" },
  { href: "/admin/orders", label: "Заказы" },
  { href: "/admin/devices", label: "Устройства" },
  { href: "/admin/scenarios", label: "Сценарии" },
  { href: "/admin/analytics", label: "Аналитика" },
  { href: "/admin/alerts", label: "Алерты" }
];

export function AdminShell({ title, children }: { title: string; children: ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-slate-100 dark:bg-slate-950">
      <header className="border-b bg-white/70 backdrop-blur dark:bg-slate-900/70">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <span className="text-xl font-semibold">SmartLocker Back-office</span>
          <nav className="flex items-center gap-4 text-sm">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-md px-3 py-2 ${
                  pathname.startsWith(item.href)
                    ? "bg-primary text-white"
                    : "text-muted hover:bg-primary/10"
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-10">
        <h1 className="text-3xl font-semibold mb-6">{title}</h1>
        <div className="grid gap-6">{children}</div>
      </main>
    </div>
  );
}
