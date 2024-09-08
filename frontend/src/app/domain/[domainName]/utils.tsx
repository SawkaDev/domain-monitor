import { DomainInfo } from "@/types/domain";

export async function fetchDomainInfo(domainName: string): Promise<DomainInfo> {
  return {
    dnsHistory: [
      {
        date: "2023-09-01",
        changeType: "A Record Added",
        oldValue: "",
        newValue: "192.0.2.1",
      },
      {
        date: "2023-08-15",
        changeType: "MX Record Changed",
        oldValue: "old-mail.example.com",
        newValue: "mail.example.com",
      },
    ],
    whoisHistory: [
      {
        date: "2022-01-01",
        registrar: "Old Registrar, Inc.",
        expirationDate: "2024-01-01",
        nameServers: ["old-ns1.example.com", "old-ns2.example.com"],
      },
      {
        date: "2020-01-01",
        registrar: "Initial Registrar, Inc.",
        expirationDate: "2022-01-01",
        nameServers: ["initial-ns1.example.com", "initial-ns2.example.com"],
      },
    ],
    monitoredSince: "2023-01-01",
    lastMonitored: "2023-09-07T15:30:00Z",
  };
}
