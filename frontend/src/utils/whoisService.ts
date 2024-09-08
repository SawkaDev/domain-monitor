import axios from "axios";

const API_URL = "http://localhost:5002/api/v1";

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

const fetchWhoIs = async (domain: string) => {
  try {
    const response = await api.get(`/whois/${domain}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching Whois:", error);
    throw new Error("Failed to fetch Whois");
  }
};

const fetchWhoIsHistory = async (domain: string) => {
  try {
    const response = await api.get(`/whois/history/${domain}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching history:", error);
    throw new Error("Failed to fetch history");
  }
};

export const WhoIsService = {
  fetchWhoIs,
  fetchWhoIsHistory,
};
