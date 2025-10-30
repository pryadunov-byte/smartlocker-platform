import { AdminShell } from "@/components/shell";
import { AlertsFeed } from "@/components/alerts-feed";

export default function AlertsPage() {
  return (
    <AdminShell title="Мониторинг и оповещения">
      <div className="card">
        <h2 className="text-lg font-semibold">Настройки подписок</h2>
        <p className="text-sm text-muted">
          Управляйте ролями и каналами уведомлений: SMS, e-mail, Telegram Bot. Назначьте ответственных для эскалаций.
        </p>
      </div>
      <AlertsFeed />
    </AdminShell>
  );
}
