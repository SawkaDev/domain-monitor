"use client";
import { useState, useEffect } from "react";
import { Loading } from "@/components/ui/Loading";
import { DomainService } from "@/utils/domainService";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { Domain, DomainResponse } from "@/types/domain";

const DOMAINS_PER_PAGE = 5;

export default function Home() {
  const [page, setPage] = useState(1);
  const [allDomains, setAllDomains] = useState<Domain[]>([]);
  const [totalDomains, setTotalDomains] = useState(0);

  const { data, isLoading, error, isFetching } = useQuery<
    DomainResponse,
    Error
  >({
    queryKey: ["domains", page],
    queryFn: () => DomainService.fetchDomains(page, DOMAINS_PER_PAGE),
    refetchOnWindowFocus: true,
  });

  useEffect(() => {
    if (data) {
      setAllDomains((prevDomains) => {
        const newDomains = data.domains.filter(
          (domain) =>
            !prevDomains.some((prevDomain) => prevDomain.id === domain.id)
        );
        return [...prevDomains, ...newDomains];
      });

      setTotalDomains((prevTotal) => Math.max(prevTotal, data.total));
    }
  }, [data]);

  const loadMore = () => {
    setPage((prevPage) => prevPage + 1);
  };

  if (isLoading && page === 1) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="text-center text-red-500 p-4">
        <p className="text-xl font-bold">An error occurred</p>
        <p>{(error as Error).message}</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-12 p-4">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-text-primary">
          Domain Feed
        </h1>
        <p className="text-xl text-text-secondary max-w-2xl mx-auto">
          Currently monitoring DNS/WHOIS changes for{" "}
          <span className="inline-flex items-center justify-center bg-blue-100 text-blue-800 text-2xl font-bold rounded-md px-3 py-1 min-w-[3rem]">
            {totalDomains}
          </span>{" "}
          domains.
        </p>
      </section>
      <section className="space-y-4">
        {allDomains.length > 0 ? (
          allDomains.map((item) => (
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
            No domains found. Search for a domain to add it to the monitoring
            service.
          </div>
        )}
      </section>

      {allDomains.length < totalDomains && (
        <section className="text-center">
          <button
            onClick={loadMore}
            disabled={isFetching}
            className="btn-primary bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition-colors"
          >
            {isFetching ? "Loading more..." : "Load More"}
          </button>
        </section>
      )}
    </div>
  );
}
