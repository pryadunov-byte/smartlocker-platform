import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-6 text-center">
      <h1 className="text-4xl font-bold">SmartLocker Platform</h1>
      <p className="max-w-xl text-muted">
        Управляйте сетью постаматов, отслеживайте заказы и предоставляйте удобный клиентский опыт с помощью единой платформы.
      </p>
      <div className="flex gap-4">
        <Link className="rounded-lg bg-primary px-6 py-3 text-white" href="/admin/dashboard">
          Перейти в back-office
        </Link>
        <Link className="rounded-lg border border-primary px-6 py-3 text-primary" href="/device-sim">
          Открыть эмулятор устройства
        </Link>
      </div>
    </main>
  );
}
