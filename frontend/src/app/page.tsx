"use client";
import { Loading } from "@/components/ui/Loading";
import { fetchDomains } from "@/utils/domainService";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

export default function Home() {
  const {
    data: domains,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["domains"],
    queryFn: fetchDomains,
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
    <div className="space-y-12 p-4">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-text-primary">
          Welcome to Domain Monitor
        </h1>
        <p className="text-xl text-text-secondary max-w-2xl mx-auto">
          View historical domain data and more!
        </p>
      </section>
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {domains && domains.length > 0 ? (
          domains.map((item) => (
            <div
              key={item.id}
              className="bg-surface p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
            >
              <h2 className="text-xl font-semibold mb-2 text-text-primary">
                <Link
                  href={`/domain/${item.id}`}
                  className="text-text-secondary hover:text-text-primary transition-colors"
                >
                  {item.name}
                </Link>
              </h2>
              <p className="text-text-secondary">ID: {item.id}</p>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center text-gray-500">
            No domains found
          </div>
        )}
      </section>

      <section className="text-center">
        <button className="btn-primary bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition-colors">
          Learn More
        </button>
      </section>
    </div>
  );
}
