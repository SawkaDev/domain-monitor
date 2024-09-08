import axios from 'axios';
import { DNSRecord } from '@/types/domain';

const DNS_API_URL = 'http://localhost:5001/api/v1';

const api = axios.create({
  baseURL: DNS_API_URL,
  timeout: 5000,
});

const fetchCurrentDNS = async (domain: string): Promise<DNSRecord[]> => {
  try {
    const response = await api.get<DNSRecord[]>(`/dns/${domain}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching current DNS for domain ${domain}:`, error);
    throw new Error(`Failed to fetch current DNS for domain ${domain}`);
  }
};

const getDNSHistory = async (domain: string) => {
  try {
    const response = await api.get(`/dns/history/${domain}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching DNS history for domain ${domain}:`, error);
    throw new Error(`Failed to fetch DNS history for domain ${domain}`);
  }
};


export const DNSService = {
  fetchCurrentDNS,
  getDNSHistory,
};
