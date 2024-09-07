import React from 'react';

interface TableHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export function TableHeader({ children, className = '' }: TableHeaderProps) {
  return (
    <th className={`px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-normal break-words ${className}`}>
      {children}
    </th>
  );
}
