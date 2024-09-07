export function TabButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
        active ? 'bg-white text-black' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
      }`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}