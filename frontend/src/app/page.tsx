"use client";
import { Loading } from "@/components/ui/Loading";
import { DomainService } from "@/utils/domainService";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

export default function Home() {
  const {
    data: domains,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["domains"],
    queryFn: DomainService.fetchDomains,
  });

  if (isLoading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="text-center text-red-500 p-4">
        <p className="text-xl font-bold">An error occurred</p>
        <p>{error.message}</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-12 p-4">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-text-primary">
          Domain Monitor Feed
        </h1>
        <p className="text-xl text-text-secondary max-w-2xl mx-auto">
          Recent domain updates and changes
        </p>
      </section>
      <section className="space-y-4">
        {domains && domains.length > 0 ? (
          domains.map((item) => (
            <div
              key={item.id}
              className="bg-surface p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow flex justify-between items-center"
            >
              <div>
                <h2 className="text-xl font-semibold text-text-primary">
                  <Link
                    href={`/domain/${item.name}`}
                    className="hover:underline"
                  >
                    {item.name}
                  </Link>
                </h2>
                <p className="text-sm text-text-secondary">ID: {item.id}</p>
              </div>
              <Link
                href={`/domain/${item.name}`}
                className="btn-secondary bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded transition-colors"
              >
                View Details
              </Link>
            </div>
          ))
        ) : (
          <div className="text-center text-gray-500">
            No domains found
          </div>
        )}
      </section>

      <section className="text-center">
        <button className="btn-primary bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition-colors">
          Load More
        </button>
      </section>
    </div>
  );
}
