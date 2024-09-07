import React, { useState } from 'react';

interface NotificationPopupProps {
  domainName: string;
  onClose: () => void;
  onNotification: (message: string, type: 'success' | 'error') => void;
}

export const NotificationPopup: React.FC<NotificationPopupProps> = ({ 
  domainName, 
  onClose,
  onNotification 
}) => {
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => {
        setTimeout(() => {
          // Simulate a subscription request
          // reject(new Error("Failed to subscribe"));
          resolve(true);
        }, 1000);
      });
      onNotification(`Successfully subscribed ${email} to updates for ${domainName}`, 'success');
      setEmail("");
      onClose();
    } catch (error) {
      onNotification('An error occurred while subscribing. Please try again.', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex justify-center items-center">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">Get Domain Updates</h3>
        <p className="text-gray-600 mb-6">Stay informed about changes to {domainName}</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex items-center border-b border-gray-300 py-2">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              className="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none"
              required
              disabled={isSubmitting}
            />
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 rounded-md disabled:opacity-50"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-md disabled:opacity-50"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Subscribing...' : 'Subscribe'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
