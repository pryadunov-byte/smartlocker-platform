import { AdminShell } from "@/components/shell";
import { AnalyticsCharts } from "@/components/analytics-charts";

export default function AnalyticsPage() {
  return (
    <AdminShell title="Аналитика">
      <div className="card">
        <p className="text-sm text-muted">
          Отчёты по заполненности, динамике просрочек и ROMI по каналам уведомлений. Данные обновляются в реальном времени.
        </p>
      </div>
      <AnalyticsCharts />
    </AdminShell>
  );
}
