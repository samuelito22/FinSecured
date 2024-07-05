import React from "react";

import { MainLayout } from "@components/layout";
import {
    Citations,
    SearchAnswers,
    SearchInput,
} from "@features/rag-search/components";
import { useSearchResponse } from "@features/rag-search/api/retrieve-search-response";
import { RegulationEnum } from "@customTypes/api";
import { Seperator } from "@components/seperator";
import { TrafficCone } from "@components/svg";
import clsx from "clsx";
import Link from "next/link";
import { useRouter } from "next/router";

const ErrorBody = (): React.JSX.Element => {
    return (
        <div className="flex-1 flex flex-col justify-center items-center w-full h-full min-h-[300px]">
            <TrafficCone className="size-14 fill-gray-500" />
            <div className="mt-5 flex flex-col space-y-3 text-center max-w-lg">
                <h1 className="font-bold text-base">Something Went Wrong</h1>
                <p className="font-light text-xs text-gray-700">
                    FinSecured has encountered an error. If this problem
                    persist, contact us at{" "}
                    <Link
                        className="underline hover:decoration-dotted underline-offset-1"
                        href="mailto:finsecured.compliance@outlook.com"
                    >
                        finsecured.compliance@outlook.com
                    </Link>
                </p>
            </div>
        </div>
    );
};

const Search: React.FC = (): React.JSX.Element => {
    const searchResponseMutation = useSearchResponse();
    const { query } = useRouter();

    const handleSearch = (query: string, regulation: RegulationEnum) => {
        if (query.trim().length > 0)
            searchResponseMutation.mutate({ data: { query, regulation } });
    };

    const isLoading =
        searchResponseMutation.isPending &&
        !!(typeof query.q === "string" && query.q.trim().length > 0);

    return (
        <MainLayout>
            <section className="container mx-auto py-8 px-5 flex flex-col flex-grow ">
                <div className="flex flex-col items-center max-w-2xl m-auto w-full">
                    <div className="w-full mt-4 flex flex-col gap-y-5">
                        <SearchInput handleSearch={handleSearch} />
                    </div>
                </div>
                {(searchResponseMutation.isError ||
                    (!isLoading && !searchResponseMutation.data)) && (
                    <ErrorBody />
                )}
                <div className="flex flex-col items-center max-w-4xl mx-auto mt-5 w-full">
                    <SearchAnswers
                        isLoading={isLoading}
                        answer={
                            searchResponseMutation.data?.success
                                ? searchResponseMutation.data.data.answer
                                : undefined
                        }
                        className="px-3"
                    />
                    {(isLoading || searchResponseMutation.isSuccess) && (
                        <Seperator className="my-4" />
                    )}
                    <Citations
                        className="px-3"
                        data={
                            searchResponseMutation.data?.success
                                ? searchResponseMutation.data.data.citations
                                : undefined
                        }
                        isLoading={isLoading}
                    />
                </div>
                <div
                    className={clsx(
                        "flex flex-col justify-end mt-6 max-w-2xl mx-auto w-full",
                        !searchResponseMutation.isError && "flex-1",
                    )}
                >
                    <span className="text-center text-xs text-gray-400 font-light">
                        FinSecured aims for accuracy in financial analysis but
                        errors can occur. We advise you to verify the
                        information provided. Responses may take time as we
                        ensure they are thorough and consider all relevant data.
                        Your patience is appreciated.
                    </span>
                </div>
            </section>
        </MainLayout>
    );
};

export default Search;
