import React from 'react';

export interface DNSRecord {
  type: string;
  name: string;
  value: string;
  ttl: number;
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
}

export function TabButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
        active ? 'bg-white text-black' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
      }`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export function StatCard({ title, value }: { title: string; value: string | number }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-700">{title}</h3>
      <p className="text-2xl font-bold text-black">{value}</p>
    </div>
  );
}
