import axios from 'axios';

const API_URL = 'http://localhost:5000/api/v1';
interface Domain {
  id: number;
  name: string;
}

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

const fetchDomains = async (): Promise<Domain[]> => {
  try {
    const response = await api.get<Domain[]>('/domains');
    return response.data;
  } catch (error) {
    console.error('Error fetching domains:', error);
    throw new Error('Failed to fetch domains');
  }
};

export const DomainService = {
  fetchDomains,
};
