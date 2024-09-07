import React, { useState } from 'react';
import { Tooltip } from './ToolTip';

interface TableCellProps {
  children: React.ReactNode;
  className?: string;
  maxLength?: number;
}

export function TableCell({ children, className = '', maxLength = 50 }: TableCellProps) {
  const [isTooltipVisible, setIsTooltipVisible] = useState(false);
  const content = Array.isArray(children) ? children.join(', ') : String(children);

  const truncatedContent = content.length > maxLength 
    ? content.slice(0, maxLength) + '...'
    : content;

  const showTooltip = content.length > maxLength;

  return (
    <td 
      className={`px-6 py-4 ${className}`}
      onMouseEnter={() => setIsTooltipVisible(true)}
      onMouseLeave={() => setIsTooltipVisible(false)}
    >
      {showTooltip ? (
        <Tooltip content={content} visible={isTooltipVisible}>
          <span className="cursor-help border-b border-dotted border-gray-500">
            {truncatedContent}
          </span>
        </Tooltip>
      ) : (
        content
      )}
    </td>
  );
}
