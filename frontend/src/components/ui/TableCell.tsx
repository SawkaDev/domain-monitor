import React from 'react';

interface TableCellProps {
  children: React.ReactNode;
  className?: string;
}

export function TableCell({ children, className = '' }: TableCellProps) {
  const content = Array.isArray(children) ? children.join(', ') : children;

  return (
    <td className={`px-6 py-4 whitespace-nowrap ${className}`}>
      {content}
    </td>
  );
}
