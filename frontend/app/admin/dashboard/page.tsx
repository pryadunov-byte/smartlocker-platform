import { AdminShell } from "@/components/shell";
import { KpiGrid } from "@/components/kpi-grid";
import { MapWidget } from "@/components/map-widget";
import { AlertsFeed } from "@/components/alerts-feed";
import { DeviceGrid } from "@/components/device-grid";

const demoMarkers = [
  { lat: 55.751244, lon: 37.618423, status: "online" as const },
  { lat: 59.93428, lon: 30.335099, status: "alert" as const },
  { lat: 56.838926, lon: 60.605703, status: "offline" as const }
];

export default function DashboardPage() {
  return (
    <AdminShell title="Дашборд сети">
      <KpiGrid />
      <MapWidget markers={demoMarkers} />
      <DeviceGrid />
      <AlertsFeed />
    </AdminShell>
  );
}
