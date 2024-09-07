"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { fetchDomainInfo } from "./utils";
import { DomainInfo, StatCard, TabButton } from "./components";
import { TableHeader } from "@/components/ui/TableHeader";
import { TableCell } from "@/components/ui/TableCell";

export default function DomainProfile() {
  const params = useParams();
  const domainName = params.domainName as string;
  const [domainInfo, setDomainInfo] = useState<DomainInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

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

  const daysUntilExpiration = () => {
    const today = new Date();
    const expirationDate = new Date(domainInfo.whoisInfo.expirationDate);
    const diffTime = Math.abs(expirationDate.getTime() - today.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold mb-6">{domainName}</h1>

      <div className="mb-4">
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

      <div className="bg-white shadow-md rounded-lg p-6">
        {activeTab === "overview" && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              <StatCard
                title="Current DNS Records"
                value={domainInfo.dnsRecords.length}
              />
              <StatCard
                title="DNS Changes"
                value={domainInfo.dnsHistory.length}
              />
              <StatCard
                title="Days Until Expiration"
                value={daysUntilExpiration()}
              />
              <StatCard
                title="WHOIS Changes"
                value={domainInfo.whoisHistory.length}
              />
            </div>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold mb-4">
                Current DNS Records
              </h2>
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
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold mb-4">
                Current WHOIS Information
              </h2>
              <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">
                    Registrar
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {domainInfo.whoisInfo.registrar}
                  </dd>
                </div>
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">
                    Creation Date
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {domainInfo.whoisInfo.creationDate}
                  </dd>
                </div>
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">
                    Expiration Date
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {domainInfo.whoisInfo.expirationDate}
                  </dd>
                </div>
                <div className="sm:col-span-2">
                  <dt className="text-sm font-medium text-gray-500">
                    Name Servers
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {domainInfo.whoisInfo.nameServers.join(", ")}
                  </dd>
                </div>
              </dl>
            </section>
          </>
        )}

        {activeTab === "dnsHistory" && (
          <section>
            <h2 className="text-2xl font-semibold mb-4">DNS History</h2>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <TableHeader>Date</TableHeader>
                  <TableHeader>Change Type</TableHeader>
                  <TableHeader>Old Value</TableHeader>
                  <TableHeader>New Value</TableHeader>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {domainInfo.dnsHistory.map((entry: any, index: any) => (
                  <tr key={index}>
                    <TableCell>{entry.date}</TableCell>
                    <TableCell>{entry.changeType}</TableCell>
                    <TableCell>{entry.oldValue}</TableCell>
                    <TableCell>{entry.newValue}</TableCell>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}

        {activeTab === "whoisHistory" && (
          <section>
            <h2 className="text-2xl font-semibold mb-4">WHOIS History</h2>
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
                {domainInfo.whoisHistory.map((entry, index) => (
                  <tr key={index}>
                    <TableCell>{entry.date}</TableCell>
                    <TableCell>{entry.registrar}</TableCell>
                    <TableCell>{entry.expirationDate}</TableCell>
                    <TableCell>{entry.nameServers}</TableCell>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}
      </div>
    </div>
  );
}
