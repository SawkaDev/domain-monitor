import { TableCell } from "@/components/ui/TableCell";
import { TableHeader } from "@/components/ui/TableHeader";
import { DNSHistoryEntry } from "@/types/domain";
import { formatDate } from "@/utils/utils";

interface DNSHistoryTabProps {
  dnsHistory: DNSHistoryEntry[];
}

export const DNSHistoryTab: React.FC<DNSHistoryTabProps> = ({ dnsHistory }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">DNS History</h2>
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <TableHeader>Date</TableHeader>
            <TableHeader>Change Type</TableHeader>
            <TableHeader>Old Value</TableHeader>
            <TableHeader>New Value</TableHeader>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {dnsHistory.map((entry, index) => (
            <tr key={index}>
              <TableCell>{formatDate(entry.date)}</TableCell>
              <TableCell>{entry.changeType}</TableCell>
              <TableCell>{entry.oldValue}</TableCell>
              <TableCell>{entry.newValue}</TableCell>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
