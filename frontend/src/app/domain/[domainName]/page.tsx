"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { fetchDomainInfo } from "./utils";
import { NotificationPopup } from "@/components/NotificationPopup";
import { Notification } from "@/components/Notification";
import { TabButton } from "@/components/ui/TabButton";
import { DomainInfo } from "@/types/domain";
import { OverviewTabMain } from "./components/OverviewTabMain";
import { OverviewTabSecondary } from "./components/OverviewTabSecondary";
import { DNSHistoryTab } from "./components/DNSHistoryTab";
import { WhoIsHistoryTab } from "./components/WhoIsHistoryTab";

export default function DomainProfile() {
  const params = useParams();
  const domainName = params.domainName as string;
  const [domainInfo, setDomainInfo] = useState<DomainInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");
  const [showNotificationPopup, setShowNotificationPopup] = useState(false);
  const [notification, setNotification] = useState<{
    message: string;
    type: "success" | "error";
  } | null>(null);

  useEffect(() => {
    const loadDomainInfo = async () => {
      setLoading(true);
      try {
        const info = await fetchDomainInfo(domainName);
        setDomainInfo(info);
      } catch (error) {
        console.error("Failed to fetch domain info:", error);
      } finally {
        setLoading(false);
      }
    };

    loadDomainInfo();
  }, [domainName]);

  const handleNotification = (message: string, type: "success" | "error") => {
    setNotification({ message, type });
  };

  if (loading) {
    return <div className="container mx-auto px-4 py-8">Loading...</div>;
  }

  if (!domainInfo) {
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

      {activeTab === "overview" && <OverviewTabMain domainInfo={domainInfo} />}

      <div className="bg-white shadow rounded-lg p-6">
        {activeTab === "overview" && (
          <OverviewTabSecondary domainInfo={domainInfo} />
        )}
        {activeTab === "dnsHistory" && (
          <DNSHistoryTab dnsHistory={domainInfo.dnsHistory} />
        )}
        {activeTab === "whoisHistory" && (
          <WhoIsHistoryTab whoisHistory={domainInfo.whoisHistory} />
        )}
      </div>
    </div>
  );
}
