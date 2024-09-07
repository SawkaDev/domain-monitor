import { TableCell } from "@/components/ui/TableCell";
import { TableHeader } from "@/components/ui/TableHeader";
import { DomainInfo } from "@/types/domain";

interface OverviewTabSecondaryProps {
  domainInfo: DomainInfo;
}

export const OverviewTabSecondary: React.FC<OverviewTabSecondaryProps> = ({
  domainInfo,
}) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Current DNS Records</h2>
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <TableHeader>Type</TableHeader>
            <TableHeader>Name</TableHeader>
            <TableHeader>Value</TableHeader>
            <TableHeader>TTL</TableHeader>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {domainInfo.dnsRecords.map((record, index) => (
            <tr key={index}>
              <TableCell>{record.type}</TableCell>
              <TableCell>{record.name}</TableCell>
              <TableCell>{record.value}</TableCell>
              <TableCell>{record.ttl}</TableCell>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
