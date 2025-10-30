import { AdminShell } from "@/components/shell";
import { OrdersTable } from "@/components/orders-table";

export default function OrdersPage() {
  return (
    <AdminShell title="Заказы и операции">
      <div className="card flex flex-wrap items-end gap-4">
        <div>
          <h2 className="text-lg font-semibold">Фильтры</h2>
          <p className="text-sm text-muted">Статус, период, устройство, услуга</p>
        </div>
        <button className="rounded-lg bg-primary px-4 py-2 text-white">Создать заказ</button>
      </div>
      <OrdersTable />
    </AdminShell>
  );
}
