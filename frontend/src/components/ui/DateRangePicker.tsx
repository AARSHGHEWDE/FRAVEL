interface DateRangePickerProps {
  startDate: string;
  endDate: string;
  onStartChange: (date: string) => void;
  onEndChange: (date: string) => void;
}

export default function DateRangePicker({
  startDate,
  endDate,
  onStartChange,
  onEndChange,
}: DateRangePickerProps) {
  return (
    <div className="flex gap-3">
      <div className="flex-1 flex flex-col gap-1.5">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          Departure
        </label>
        <input
          type="date"
          value={startDate}
          onChange={(e) => onStartChange(e.target.value)}
          className="w-full rounded-xl border border-surface-200 bg-white px-4 py-2.5 text-surface-900 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 dark:border-surface-700 dark:bg-surface-900 dark:text-surface-50 transition-colors"
        />
      </div>
      <div className="flex-1 flex flex-col gap-1.5">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          Return
        </label>
        <input
          type="date"
          value={endDate}
          min={startDate}
          onChange={(e) => onEndChange(e.target.value)}
          className="w-full rounded-xl border border-surface-200 bg-white px-4 py-2.5 text-surface-900 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 dark:border-surface-700 dark:bg-surface-900 dark:text-surface-50 transition-colors"
        />
      </div>
    </div>
  );
}
