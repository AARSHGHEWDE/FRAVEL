import { motion } from "framer-motion";

interface AgentProgressRingProps {
  progress: number; // 0 to 1
  size?: number;
}

export default function AgentProgressRing({ progress, size = 120 }: AgentProgressRingProps) {
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - progress * circumference;

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          fill="none"
          className="stroke-surface-200 dark:stroke-surface-800"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          className="stroke-primary-500"
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          strokeDasharray={circumference}
        />
      </svg>
      <span className="absolute text-2xl font-bold font-display text-primary-600 dark:text-primary-400">
        {Math.round(progress * 100)}%
      </span>
    </div>
  );
}
