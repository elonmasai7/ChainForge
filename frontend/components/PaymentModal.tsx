export function PaymentModal() {
  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold">Complete Payment</h3>
      <p className="mt-2 text-black/60">Confirm subscription via Initia wallet.</p>
      <div className="mt-4 flex items-center gap-3">
        <span className="badge">Pending</span>
        <span className="text-sm text-black/50">Tx: initia1...9f2</span>
      </div>
      <button className="card mt-6 px-4 py-2">Confirm</button>
    </div>
  );
}
