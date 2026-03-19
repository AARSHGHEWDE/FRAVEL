import { motion } from "framer-motion";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
}

const sizes = { sm: "h-4 w-4", md: "h-8 w-8", lg: "h-12 w-12" };

export default function LoadingSpinner({ size = "md" }: LoadingSpinnerProps) {
  return (
    <motion.div
      className={`${sizes[size]} rounded-full border-2 border-surface-200 border-t-primary-600 dark:border-surface-700 dark:border-t-primary-400`}
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
    />
  );
}
