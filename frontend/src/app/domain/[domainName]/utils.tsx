import { DomainInfo } from './components';

export async function fetchDomainInfo(domainName: string): Promise<DomainInfo> {
  return {
    dnsRecords: [
      { type: 'A', name: domainName, value: '192.0.2.1', ttl: 3600 },
      { type: 'MX', name: domainName, value: 'mail.example.com', ttl: 3600 },
    ],
    dnsHistory: [
      { date: '2023-09-01', changeType: 'A Record Added', oldValue: '', newValue: '192.0.2.1' },
      { date: '2023-08-15', changeType: 'MX Record Changed', oldValue: 'old-mail.example.com', newValue: 'mail.example.com' },
    ],
    whoisInfo: {
      registrar: 'Example Registrar, Inc.',
      creationDate: '2020-01-01',
      expirationDate: '2025-01-01',
      nameServers: ['ns1.example.com', 'ns2.example.com'],
    },
    whoisHistory: [
      {
        date: '2022-01-01',
        registrar: 'Old Registrar, Inc.',
        expirationDate: '2024-01-01',
        nameServers: ['old-ns1.example.com', 'old-ns2.example.com'],
      },
      {
        date: '2020-01-01',
        registrar: 'Initial Registrar, Inc.',
        expirationDate: '2022-01-01',
        nameServers: ['initial-ns1.example.com', 'initial-ns2.example.com'],
      },
    ],
  };
}
