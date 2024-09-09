import { DomainStats, DomainValidity } from "@/types/domain";
import axios from "axios";

const API_URL = "http://localhost:5000/api/v1";
interface Domain {
  id: number;
  name: string;
}

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

const fetchDomains = async (
  page = 1,
  limit = 20
): Promise<{ domains: Domain[]; total: number }> => {
  try {
    const response = await api.get<{
      domains: Domain[];
      total: number;
      page: number;
      limit: number;
    }>("/domains", {
      params: { page, limit },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching domains:", error);
    throw new Error("Failed to fetch domains");
  }
};

const fetchStats = async (domainName: string): Promise<DomainStats> => {
  try {
    const response = await api.get(`/domain/stats/${domainName}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching domains:", error);
    throw new Error("Failed to fetch domains");
  }
};

const checkOrCreateDomainRecord = async (
  domainName: string
): Promise<DomainValidity> => {
  try {
    const response = await api.post(`/domain/validate`, { domain: domainName });
    return response.data;
  } catch (error) {
    console.error("Error Checking/Validating Domain:", error);
    return { exists: false, records_ready: false };
  }
};

export const DomainService = {
  fetchDomains,
  fetchStats,
  checkOrCreateDomainRecord,
};
