import { PaymentModal } from "@/components/PaymentModal";

export default function PaymentPage() {
  return (
    <main className="min-h-screen px-8 py-12">
      <h1 className="text-4xl font-semibold">Payment</h1>
      <div className="mt-8 max-w-md">
        <PaymentModal />
      </div>
    </main>
  );
}
