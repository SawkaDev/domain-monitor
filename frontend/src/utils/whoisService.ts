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
    console.error("Error fetching domains:", error);
    throw new Error("Failed to fetch domains");
  }
};

export const WhoIsService = {
  fetchWhoIs,
};
