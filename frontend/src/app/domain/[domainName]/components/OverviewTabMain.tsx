import { DomainStats, WHOISInfo } from "@/types/domain";
import { formatDate } from "@/utils/utils";

interface OverviewTabMainProps {
  currentDNSrecords: number;
  whoIsInfo: WHOISInfo;
  stats: DomainStats;
}

export const OverviewTabMain: React.FC<OverviewTabMainProps> = ({
  whoIsInfo,
  currentDNSrecords,
  stats,
}) => {
  const daysUntilExpiration = () => {
    const today = new Date();
    if (
      whoIsInfo.expiration_date === null ||
      whoIsInfo.expiration_date === undefined
    ) {
      return "n/a";
    }
    const expirationDate = new Date(whoIsInfo.expiration_date);
    const diffTime = Math.abs(expirationDate.getTime() - today.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">Domain Overview</h2>
        <div className="space-y-3">
          <p>
            <span className="font-semibold">Registrar: </span>
            {whoIsInfo.registrar || "n/a"}
          </p>
          <p>
            <span className="font-semibold">Creation Date: </span>
            {whoIsInfo.registration_date
              ? formatDate(whoIsInfo.registration_date)
              : "n/a"}
          </p>
          <p>
            <span className="font-semibold">Expiration Date: </span>
            {whoIsInfo.expiration_date
              ? formatDate(whoIsInfo.expiration_date)
              : "n/a"}
          </p>
          <p>
            <span className="font-semibold">Days Until Expiration: </span>
            {daysUntilExpiration()}
          </p>
          <p>
            <span className="font-semibold">Name Servers: </span>
            {whoIsInfo.nameservers && whoIsInfo.nameservers.length > 0 ? (
              <span className="break-all">
                {whoIsInfo.nameservers}
              </span>
            ) : (
              "n/a"
            )}
          </p>
        </div>
      </div>
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">Monitoring Information</h2>
        <div className="space-y-3">
          <p>
            <span className="font-semibold">Monitored Since: </span>
            {formatDate(stats.created_at)}
          </p>
          <p>
            <span className="font-semibold">Most Recent Update: </span>
            {new Date(stats.updated_at).toLocaleString()}
          </p>
          <p>
            <span className="font-semibold">Current DNS Records: </span>
            {currentDNSrecords}
          </p>
          <p>
            <span className="font-semibold">DNS Changes: </span>
            {stats.dns_changes}
          </p>
          <p>
            <span className="font-semibold">WHOIS Changes: </span>
            {stats.whois_changes}
          </p>
        </div>
      </div>
    </div>
  );
};
