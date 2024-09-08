import { DomainInfo, WHOISInfo } from "@/types/domain";
import { formatDate } from "@/utils/utils";

interface OverviewTabMainProps {
  domainInfo: DomainInfo;
  currentDNSrecords: number;
  whoIsInfo: WHOISInfo;
}

export const OverviewTabMain: React.FC<OverviewTabMainProps> = ({
  domainInfo,
  whoIsInfo,
  currentDNSrecords,
}) => {
  const daysUntilExpiration = () => {
    const today = new Date();
    if (whoIsInfo.expiration_date === null) {
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
            {whoIsInfo.registrar}
          </p>
          <p>
            <span className="font-semibold">Creation Date: </span>
            {formatDate(whoIsInfo.registration_date)}
          </p>
          <p>
            <span className="font-semibold">Expiration Date: </span>
            {formatDate(whoIsInfo.expiration_date)}
          </p>
          <p>
            <span className="font-semibold">Days Until Expiration: </span>
            {daysUntilExpiration()}
          </p>
          <p>
            <span className="font-semibold">Name Servers: </span>
            {whoIsInfo.nameservers}
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
            {currentDNSrecords ? currentDNSrecords : 0}
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
