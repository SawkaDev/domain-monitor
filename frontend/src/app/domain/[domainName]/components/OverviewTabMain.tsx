import { DomainInfo } from "@/types/domain";
import { formatDate } from "@/utils/utils";

interface OverviewTabMainProps {
  domainInfo: DomainInfo;
}

export const OverviewTabMain: React.FC<OverviewTabMainProps> = ({
  domainInfo,
}) => {
  const daysUntilExpiration = () => {
    const today = new Date();
    const expirationDate = new Date(domainInfo.whoisInfo.expirationDate);
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
            {domainInfo.whoisInfo.registrar}
          </p>
          <p>
            <span className="font-semibold">Creation Date: </span>
            {formatDate(domainInfo.whoisInfo.creationDate)}
          </p>
          <p>
            <span className="font-semibold">Expiration Date: </span>
            {formatDate(domainInfo.whoisInfo.expirationDate)}
          </p>
          <p>
            <span className="font-semibold">Days Until Expiration: </span>
            {daysUntilExpiration()}
          </p>
          <p>
            <span className="font-semibold">Name Servers: </span>
            {domainInfo.whoisInfo.nameServers.join(", ")}
          </p>
        </div>
      </div>
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">Monitoring Information</h2>
        <div className="space-y-3">
          <p>
            <span className="font-semibold">Monitored Since: </span>
            {formatDate(domainInfo.monitoredSince)}
          </p>
          <p>
            <span className="font-semibold">Last Monitored: </span>
            {new Date(domainInfo.lastMonitored).toLocaleString()}
          </p>
          <p>
            <span className="font-semibold">Current DNS Records: </span>
            {domainInfo.dnsRecords.length}
          </p>
          <p>
            <span className="font-semibold">DNS Changes: </span>
            {domainInfo.dnsHistory.length}
          </p>
          <p>
            <span className="font-semibold">WHOIS Changes: </span>
            {domainInfo.whoisHistory.length}
          </p>
        </div>
      </div>
    </div>
  );
};
