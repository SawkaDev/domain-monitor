import React from "react";

interface TooltipProps {
  children: React.ReactNode;
  content: string;
  visible: boolean;
}

export function Tooltip({ children, content, visible }: TooltipProps) {
  return (
    <div className="relative inline-block">
      {children}
      {visible && (
        <div className="absolute z-10 p-2 -mt-1 text-sm text-white bg-gray-800 rounded-lg shadow-lg whitespace-normal">
          {content}
        </div>
      )}
    </div>
  );
}
