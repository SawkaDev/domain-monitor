import { Notification } from "@/types/notification";
import axios from "axios";

const API_URL = "http://localhost:8080/notification-service/api/v1";

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

const getAllNotifications = async (): Promise<Notification[]> => {
  try {
    const response = await api.get<{ notifications: Notification[] }>(
      "/all"
    );
    return response.data.notifications;
  } catch (error) {
    console.error("Error fetching all notifications:", error);
    throw new Error("Failed to fetch all notifications");
  }
};

const getUserNotifications = async (email: string): Promise<Notification[]> => {
  try {
    const response = await api.get<{ notifications: Notification[] }>(
      `/all/user/${email}`
    );
    return response.data.notifications;
  } catch (error) {
    console.error("Error fetching user notifications:", error);
    throw new Error("Failed to fetch user notifications");
  }
};

const addNotification = async (
  domain_name: string,
  email: string
): Promise<Notification> => {
  try {
    const response = await api.post<Notification>("/", {
      domain_name,
      email,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 409) {
      throw new Error("Notification already exists");
    }
    console.error("Error adding notification:", error);
    throw new Error("Failed to add notification");
  }
};

const removeNotification = async (
  domain_name: string,
  email: string
): Promise<void> => {
  try {
    await api.delete("/", { data: { domain_name, email } });
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      throw new Error("Notification not found");
    }
    console.error("Error removing notification:", error);
    throw new Error("Failed to remove notification");
  }
};

const checkHeartbeat = async (): Promise<boolean> => {
  try {
    const response = await api.get("/heartbeat");
    return response.data.status === "ok";
  } catch (error) {
    console.error("Error checking heartbeat:", error);
    return false;
  }
};

export const NotificationService = {
  getAllNotifications,
  getUserNotifications,
  addNotification,
  removeNotification,
  checkHeartbeat,
};
