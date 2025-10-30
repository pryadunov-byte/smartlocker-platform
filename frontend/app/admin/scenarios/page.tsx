import { AdminShell } from "@/components/shell";

const scenarioFields = [
  { label: "Срок хранения", value: "72 часа" },
  { label: "Тариф", value: "15 ₽/час" },
  { label: "Штраф", value: "50 ₽" },
  { label: "Уведомления", value: "SMS, E-mail" },
  { label: "Параметры замка", value: "Unlock 5s, Delay 2s, WaitDoor 15s" }
];

export default function ScenariosPage() {
  return (
    <AdminShell title="Сценарии и правила">
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="card space-y-3">
          <h2 className="text-lg font-semibold">No-code конфигуратор</h2>
          {scenarioFields.map((item) => (
            <div key={item.label} className="flex items-center justify-between rounded-lg bg-slate-100 p-3 text-sm dark:bg-slate-800/80">
              <span className="text-muted">{item.label}</span>
              <span className="font-medium">{item.value}</span>
            </div>
          ))}
          <button className="rounded-lg bg-primary px-4 py-2 text-white">Создать сценарий</button>
        </div>
        <div className="card">
          <h2 className="text-lg font-semibold">Шаблоны уведомлений</h2>
          <ul className="space-y-3 text-sm">
            <li className="rounded-lg border border-slate-200 p-3 dark:border-slate-700">
              <strong>order_arrived</strong> — приветствие клиента с короткой ссылкой
            </li>
            <li className="rounded-lg border border-slate-200 p-3 dark:border-slate-700">
              <strong>reminder_before_expiry</strong> — напоминание за 6 часов до просрочки
            </li>
            <li className="rounded-lg border border-slate-200 p-3 dark:border-slate-700">
              <strong>expired_notice</strong> — уведомление о просрочке и размере штрафа
            </li>
          </ul>
        </div>
      </div>
    </AdminShell>
  );
}
