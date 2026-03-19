import { motion, type HTMLMotionProps } from "framer-motion";
import type { ReactNode } from "react";

interface CardProps extends HTMLMotionProps<"div"> {
  children: ReactNode;
  hover?: boolean;
  glass?: boolean;
}

export default function Card({ children, hover = false, glass = false, className = "", ...props }: CardProps) {
  return (
    <motion.div
      whileHover={hover ? { y: -2, scale: 1.01 } : undefined}
      className={`
        rounded-2xl border p-6
        ${glass
          ? "border-white/20 bg-white/10 backdrop-blur-xl dark:border-white/10 dark:bg-white/5"
          : "border-surface-200 bg-white dark:border-surface-800 dark:bg-surface-900"
        }
        shadow-sm ${hover ? "cursor-pointer" : ""} ${className}
      `}
      {...props}
    >
      {children}
    </motion.div>
  );
}
