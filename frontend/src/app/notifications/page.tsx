"use client";

import { Loading } from "@/components/ui/Loading";
import { NotificationService } from "@/utils/notificationService";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { FaTrash } from "react-icons/fa";

interface Notification {
  id: number;
  domain_name: string;
  email: string;
  created_at: string;
}

function NotificationsTable() {
  const queryClient = useQueryClient();

  const {
    data: notifications,
    isLoading,
    error,
  } = useQuery<Notification[], Error>({
    queryKey: ["notifications"],
    queryFn: NotificationService.getAllNotifications,
  });

  const unsubscribeMutation = useMutation({
    mutationFn: ({
      domain_name,
      email,
    }: {
      domain_name: string;
      email: string;
    }) => NotificationService.removeNotification(domain_name, email),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] });
    },
  });

  const handleUnsubscribe = (domain_name: string, email: string) => {
    unsubscribeMutation.mutate({ domain_name, email });
  };

  if (isLoading) return <Loading />;

  if (error)
    return (
      <div
        className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
        role="alert"
      >
        {error.message}
      </div>
    );

  const notificationCount = notifications?.length || 0;

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200 flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-800">
          Current Notification
        </h1>
        <span className="bg-blue-500 text-white text-sm font-bold px-3 py-1 rounded-full">
          {notificationCount}
        </span>
      </div>
      {notifications && notifications.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Domain
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Email
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Subscribed On
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {notifications.map((notification) => (
                <tr key={notification.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {notification.domain_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {notification.email}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(notification.created_at).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() =>
                        handleUnsubscribe(
                          notification.domain_name,
                          notification.email
                        )
                      }
                      className="text-red-600 hover:text-red-900 focus:outline-none focus:underline flex items-center"
                      disabled={unsubscribeMutation.isPending}
                    >
                      <FaTrash className="mr-2" />
                      {unsubscribeMutation.isPending
                        ? "Unsubscribing..."
                        : "Unsubscribe"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="px-6 py-4 text-center text-gray-500">
          No notifications found. Please click Get Notifications on any domain
          profile page to subscribe.
        </div>
      )}
    </div>
  );
}

export default function NotificationsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <NotificationsTable />
    </div>
  );
}
