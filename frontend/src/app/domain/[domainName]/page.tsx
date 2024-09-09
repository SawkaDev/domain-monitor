"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { NotificationPopup } from "@/components/NotificationPopup";
import { Notification } from "@/components/Notification";
import { TabButton } from "@/components/ui/TabButton";
import { OverviewTabMain } from "./components/OverviewTabMain";
import { OverviewTabSecondary } from "./components/OverviewTabSecondary";
import { DNSHistoryTab } from "./components/DNSHistoryTab";
import { WhoIsHistoryTab } from "./components/WhoIsHistoryTab";
import { Loading } from "@/components/ui/Loading";
import { DNSService } from "@/utils/dnsService";
import { WhoIsService } from "@/utils/whoisService";
import { DomainService } from "@/utils/domainService";
import { DomainValidity } from "@/types/domain";

export default function DomainProfile() {
  const params = useParams();
  const domainName = params.domainName as string;
  const [activeTab, setActiveTab] = useState("overview");
  const [showNotificationPopup, setShowNotificationPopup] = useState(false);
  const [notification, setNotification] = useState<{
    message: string;
    type: "success" | "error";
  } | null>(null);

  const [isReadyForQueries, setIsReadyForQueries] = useState(false);

  const {
    data: valid,
    isLoading: validLoading,
    isError: isValidError,
    error: validError,
    refetch: refetchValidation,
  } = useQuery<DomainValidity, Error>({
    queryKey: ["validateDomain", domainName],
    queryFn: () => DomainService.checkOrCreateDomainRecord(domainName),
    enabled: !!domainName,
    staleTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
  });

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (valid && valid.exists) {
      if (!valid.records_ready) {
        timer = setInterval(() => {
          refetchValidation();
        }, 5000);
      } else {
        setIsReadyForQueries(true);
      }
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [valid, refetchValidation]);

  const {
    data: currentDNS,
    isLoading: dnsLoading,
    isError: isDNSError,
    error: dnsError,
  } = useQuery({
    queryKey: ["currentDNS", domainName],
    queryFn: () => DNSService.fetchCurrentDNS(domainName),
    enabled: isReadyForQueries,
  });

  const {
    data: currentWhois,
    isLoading: whoisLoading,
    isError: isWhoisError,
    error: whoisError,
  } = useQuery({
    queryKey: ["whoisData", domainName],
    queryFn: () => WhoIsService.fetchWhoIs(domainName),
    enabled: isReadyForQueries,
  });

  const {
    data: domainStats,
    isLoading: domainStatsLoading,
    isError: isDomainStatsError,
    error: domainStatsError,
  } = useQuery({
    queryKey: ["stats", domainName],
    queryFn: () => DomainService.fetchStats(domainName),
    enabled: isReadyForQueries,
  });

  const handleNotification = (message: string, type: "success" | "error") => {
    setNotification({ message, type });
  };

  if (validLoading) {
    return <Loading />;
  }

  if (isValidError) {
    return (
      <div className="container mx-auto px-4 py-8">
        Error validating domain: {validError.message}
      </div>
    );
  }

  if (!valid?.exists) {
    return (
      <div className="container mx-auto px-4 py-8">
        Domain does not exist in our records.
      </div>
    );
  }

  if (!isReadyForQueries) {
    return <Loading text="New domain to monitor! Records are being prepared. Please wait..." />;

  }

  if (dnsLoading || whoisLoading || domainStatsLoading) {
    return <Loading />;
  }

  if (isDNSError || isWhoisError || isDomainStatsError) {
    return (
      <div className="container mx-auto px-4 py-8">
        {isDNSError && <p>Error loading DNS data: {dnsError.message}</p>}
        {isWhoisError && <p>Error loading WHOIS data: {whoisError.message}</p>}
        {isDomainStatsError && (
          <p>Error loading domain stats: {domainStatsError.message}</p>
        )}
      </div>
    );
  }

  if (!currentDNS || !currentWhois || !domainStats) {
    return (
      <div className="container mx-auto px-4 py-8">
        No information found for this domain.
      </div>
    );
  }
  return (
    <div className="container mx-auto px-4 py-8 relative">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">
          <Link
            href={`https://${domainName}`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 transition-colors duration-500"
          >
            {domainName}
          </Link>
        </h1>
        <button
          onClick={() => setShowNotificationPopup(true)}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Get Notifications
        </button>
      </div>

      {showNotificationPopup && (
        <NotificationPopup
          domainName={domainName}
          onClose={() => setShowNotificationPopup(false)}
          onNotification={handleNotification}
        />
      )}

      {notification && (
        <Notification
          message={notification.message}
          type={notification.type}
          onClose={() => setNotification(null)}
        />
      )}
      <div className="mb-6 flex space-x-2">
        <TabButton
          active={activeTab === "overview"}
          onClick={() => setActiveTab("overview")}
        >
          Overview
        </TabButton>
        <TabButton
          active={activeTab === "dnsHistory"}
          onClick={() => setActiveTab("dnsHistory")}
        >
          DNS History
        </TabButton>
        <TabButton
          active={activeTab === "whoisHistory"}
          onClick={() => setActiveTab("whoisHistory")}
        >
          WHOIS History
        </TabButton>
      </div>
      {activeTab === "overview" && (
        <OverviewTabMain
          currentDNSrecords={currentDNS ? currentDNS.length : 0}
          whoIsInfo={currentWhois}
          stats={domainStats}
        />
      )}

      <div className="bg-white shadow rounded-lg p-6">
        {activeTab === "overview" && (
          <OverviewTabSecondary dnsRecords={currentDNS ? currentDNS : []} />
        )}
        {activeTab === "dnsHistory" && (
          <DNSHistoryTab domainName={domainName} />
        )}
        {activeTab === "whoisHistory" && (
          <WhoIsHistoryTab domainName={domainName} />
        )}
      </div>
    </div>
  );
}
