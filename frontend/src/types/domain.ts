export interface DNSRecord {
  domain_id: number;
  id: number;
  last_updated: string;
  record_type: string;
  value: string;
}

export interface DNSHistoryEntry {
  timestamp: string;
  value: string;
  change_type: string;
  domain_id: string;
  record_type: string;
}

export interface WHOISInfo {
  registrar: string;
  creationDate: string;
  expirationDate: string;
  nameServers: string[];
}

export interface WHOISHistoryEntry {
  date: string;
  registrar: string;
  expirationDate: string;
  nameServers: string[];
}

export interface DomainInfo {
  dnsRecords: DNSRecord[];
  dnsHistory: DNSHistoryEntry[];
  whoisInfo: WHOISInfo;
  whoisHistory: WHOISHistoryEntry[];
  monitoredSince: string;
  lastMonitored: string;
}
