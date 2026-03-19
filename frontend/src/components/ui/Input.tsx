import { forwardRef, type InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = "", ...props }, ref) => (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          {label}
        </label>
      )}
      <input
        ref={ref}
        className={`
          w-full rounded-xl border border-surface-200 bg-white px-4 py-2.5
          text-surface-900 placeholder:text-surface-400
          focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20
          dark:border-surface-700 dark:bg-surface-900 dark:text-surface-50
          dark:placeholder:text-surface-500 dark:focus:border-primary-400
          transition-colors ${error ? "border-red-500" : ""} ${className}
        `}
        {...props}
      />
      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  )
);

Input.displayName = "Input";
export default Input;
