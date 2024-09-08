import { TableCell } from "@/components/ui/TableCell";
import { TableHeader } from "@/components/ui/TableHeader";
import { WHOISHistoryEntry } from "@/types/domain";
import { formatDate } from "@/utils/utils";
import { WhoIsService } from "@/utils/whoisService";
import { useQuery } from "@tanstack/react-query";

interface WhoIsHistoryTabProps {
  domainName: string;
}
export function formatFieldName(fieldName: string): string {
  return fieldName
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
}
export const WhoIsHistoryTab: React.FC<WhoIsHistoryTabProps> = ({
  domainName,
}) => {
  const {
    data: whoisHistory,
    isLoading,
    error,
  } = useQuery<WHOISHistoryEntry[]>({
    queryKey: ["dnsHistory", domainName],
    queryFn: () => WhoIsService.fetchWhoIsHistory(domainName),
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 5,
  });

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">WHOIS History</h2>
      {whoisHistory && whoisHistory.length == 0 && (
        <p>No DNS history found since monitoring started. </p>
      )}
      {whoisHistory && whoisHistory.length > 0 && (
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <TableHeader>Date Change</TableHeader>
              <TableHeader>Field</TableHeader>
              <TableHeader>Old Value</TableHeader>
              <TableHeader>New Value</TableHeader>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {whoisHistory.map((entry, index) => (
              <tr key={index}>
                <TableCell>
                  {new Date(entry.changed_at).toLocaleString()}
                </TableCell>
                <TableCell>{formatFieldName(entry.field_name)}</TableCell>
                <TableCell>{entry.old_value}</TableCell>
                <TableCell>{entry.new_value}</TableCell>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
