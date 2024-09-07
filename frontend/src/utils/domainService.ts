import { DNSRecord } from '@/types/domain';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api/v1';
const DNS_API_URL = 'http://localhost:5001/api/v1';

interface Domain {
  id: number;
  name: string;
}

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

const dnsApi = axios.create({
  baseURL: DNS_API_URL,
  timeout: 5000,
});

export const fetchDomains = async (): Promise<Domain[]> => {
  try {
    const response = await api.get<Domain[]>('/domains');
    return response.data;
  } catch (error) {
    console.error('Error fetching domains:', error);
    throw new Error('Failed to fetch domains');
  }
};


export const fetchCurrentDNS = async (domainId: number): Promise<DNSRecord[] | []> => {
  try {
    const response = await dnsApi.get<DNSRecord[]>(`/dns/${domainId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching current DNS for domain ID ${domainId}:`, error);
    throw new Error(`Failed to fetch current DNS for domain ID ${domainId}`);
  }
};
