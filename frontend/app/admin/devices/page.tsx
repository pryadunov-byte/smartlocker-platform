import { AdminShell } from "@/components/shell";
import { DeviceGrid } from "@/components/device-grid";

export default function DevicesPage() {
  return (
    <AdminShell title="Парк устройств">
      <div className="card">
        <h2 className="text-lg font-semibold">Редактор шкафа</h2>
        <p className="text-sm text-muted">
          Визуальная сетка ячеек с цветовым кодированием. Выберите ячейку, чтобы пометить статус или отключить услугу.
        </p>
      </div>
      <DeviceGrid />
    </AdminShell>
  );
}
