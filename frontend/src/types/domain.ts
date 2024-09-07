export interface DNSRecord {
  domain_id: number;
  id: number;
  last_updated: string;
  record_type: string;
  value: string;
}

export interface DNSHistoryEntry {
  date: string;
  changeType: string;
  oldValue: string;
  newValue: string;
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