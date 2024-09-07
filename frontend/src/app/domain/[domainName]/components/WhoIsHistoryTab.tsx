import { TableCell } from "@/components/ui/TableCell";
import { TableHeader } from "@/components/ui/TableHeader";
import { WHOISHistoryEntry } from "@/types/domain";
import { formatDate } from "@/utils/utils";

interface WhoIsHistoryTabProps {
  whoisHistory: WHOISHistoryEntry[];
}

export const WhoIsHistoryTab: React.FC<WhoIsHistoryTabProps> = ({
  whoisHistory,
}) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">WHOIS History</h2>
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <TableHeader>Date</TableHeader>
            <TableHeader>Registrar</TableHeader>
            <TableHeader>Expiration Date</TableHeader>
            <TableHeader>Name Servers</TableHeader>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {whoisHistory.map((entry, index) => (
            <tr key={index}>
              <TableCell>{formatDate(entry.date)}</TableCell>
              <TableCell>{entry.registrar}</TableCell>
              <TableCell>{formatDate(entry.expirationDate)}</TableCell>
              <TableCell>{entry.nameServers}</TableCell>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
