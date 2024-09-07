'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function SearchResults() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q');
  const [results, setResults] = useState<string[]>([]);

  useEffect(() => {
    if (query) {
      setResults([`Results for "${query}"`, 'Result 1', 'Result 2', 'Result 3']);
    }
  }, [query]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">Search Results</h1>
      {results.length > 0 ? (
        <ul className="space-y-2">
          {results.map((result, index) => (
            <li key={index} className="bg-white p-4 rounded shadow">{result}</li>
          ))}
        </ul>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}
