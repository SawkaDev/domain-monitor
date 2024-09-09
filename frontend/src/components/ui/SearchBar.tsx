"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const validateDomain = (domain: string) => {
    const domainRegex =
      /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}$/;
    return domainRegex.test(domain);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      if (validateDomain(query)) {
        setError("");
        router.push(`/domain/${encodeURIComponent(query)}`);
      } else {
        setError("Please enter a valid domain name (e.g., example.com)");
      }
    } else {
      setError("Please enter a domain name");
    }
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSearch} className="w-full flex">
        <input
          type="text"
          placeholder="Enter a domain name (e.g., example.com)"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setError(""); // Clear error when user types
          }}
          className={`w-full px-4 py-2 rounded-l-full border ${
            error ? "border-red-500" : "border-gray-300"
          } bg-white text-text-primary placeholder:text-secondary focus:outline-none focus:ring-2 ${
            error ? "focus:ring-red-500" : "focus:ring-black"
          }`}
        />
        <button
          type="submit"
          className="bg-black text-white px-4 py-2 rounded-r-full hover:bg-gray-800 transition-colors"
        >
          <SearchIcon />
        </button>
      </form>
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
}

function SearchIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="11" cy="11" r="8"></circle>
      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
  );
}
