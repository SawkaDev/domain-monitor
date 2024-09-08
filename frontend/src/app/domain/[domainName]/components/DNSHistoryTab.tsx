import React from "react";
import { useQuery } from "@tanstack/react-query";
import { TableCell } from "@/components/ui/TableCell";
import { TableHeader } from "@/components/ui/TableHeader";
import { DNSHistoryEntry } from "@/types/domain";
import { DNSService } from "@/utils/dnsService";

interface DNSHistoryTabProps {
  domainName: string;
}

export const DNSHistoryTab: React.FC<DNSHistoryTabProps> = ({ domainName }) => {
  const {
    data: dnsHistory,
    isLoading,
    error,
  } = useQuery<DNSHistoryEntry[]>({
    queryKey: ["dnsHistory", domainName],
    queryFn: () => DNSService.getDNSHistory(domainName),
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 5,
  });

  if (isLoading) return <div>Loading DNS history...</div>;
  // if (error)
  //   return <div>Error loading DNS history: {(error as Error).message}</div>;

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">
        DNS History for {domainName}
      </h2>
      {!error && dnsHistory && dnsHistory.length > 0 ? (
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <TableHeader>Date</TableHeader>
              <TableHeader>Record Type</TableHeader>
              <TableHeader>Action</TableHeader>
              <TableHeader>Value</TableHeader>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {dnsHistory.map((entry, index) => (
              <tr key={index}>
                <TableCell>
                  {new Date(entry.timestamp).toLocaleString()}
                </TableCell>
                <TableCell>{entry.record_type}</TableCell>
                <TableCell>{entry.change_type}</TableCell>
                <TableCell>{entry.value}</TableCell>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No DNS history found since monitoring started. </p>
      )}
    </div>
  );
};
