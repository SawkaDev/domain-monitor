export interface LoadingProps {
  text?: string;
}
export const Loading = ({ text }: LoadingProps) => {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="flex space-x-2 mb-4">
        <div className="w-6 h-6 bg-blue-500 rounded-full animate-pulse"></div>
        <div className="w-6 h-6 bg-blue-500 rounded-full animate-pulse delay-75"></div>
        <div className="w-6 h-6 bg-blue-500 rounded-full animate-pulse delay-150"></div>
      </div>
      <p className="text-lg text-gray-700 font-semibold">
        {text || "Loading, please wait..."}
      </p>
    </div>
  );
};
