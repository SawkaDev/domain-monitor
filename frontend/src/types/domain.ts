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
  id: number;
  domain_id: number;
  dnssec: boolean;
  registrant_country: string | null;
  registrant_locality: string | null;
  registrant_postal_code: string | null;
  registrant_region: string | null;
  registrant_street_address: string | null;
  registrant_email: string | null;
  registrant_name: string | null;
  registrant_tel: string | null;
  registrar: string | null;
  expiration_date: string | null;
  last_changed_date: string | null;
  name: string | null;
  nameservers: string | null;
  registration_date: string | null;
  status: string | null;
  terms_of_service_url: string | null;
  type: string | null;
  updated_at: string;
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
