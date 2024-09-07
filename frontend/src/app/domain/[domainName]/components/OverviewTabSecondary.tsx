import { TableCell } from "@/components/ui/TableCell";
import { TableHeader } from "@/components/ui/TableHeader";
import { DNSRecord } from "@/types/domain";

interface OverviewTabSecondaryProps {
  dnsRecords: DNSRecord[] | [];
}

export const OverviewTabSecondary: React.FC<OverviewTabSecondaryProps> = ({
  dnsRecords,
}) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Current DNS Records</h2>
      {dnsRecords.length === 0 && <p>No Current DNS Records Found</p>}
      {dnsRecords.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <TableHeader>Type</TableHeader>
                <TableHeader>Name</TableHeader>
                <TableHeader>Last Updated</TableHeader>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {dnsRecords.map((record, index) => (
                <tr key={index}>
                  <TableCell>{record.record_type}</TableCell>
                  <TableCell>{record.value}</TableCell>
                  <TableCell>
                    {new Date(record.last_updated).toLocaleString()}
                  </TableCell>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
