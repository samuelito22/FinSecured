import { Search } from "@components/svg";
import { useRouter } from "next/router";
import { ChangeEvent, FormEvent, useEffect, useState, JSX } from "react";
import { getSearchResponseInputSchema } from "../api/retrieve-search-response";
import { RegulationEnum } from "@customTypes/api";
import clsx from "clsx";

interface SearchInputProps {
    handleSearch?: (query: string, regulation: RegulationEnum) => void;
    className?: string;
}

export const SearchInput = ({
    handleSearch,
    className,
}: SearchInputProps): JSX.Element => {
    const { pathname, query, push, isReady } = useRouter();
    const [inputValue, setInputValue] = useState("");

    useEffect(() => {
        const _query = query.q as string;
        if (pathname === "/search" && _query && isReady) {
            setInputValue(_query);
            if (handleSearch) handleSearch(_query, RegulationEnum["FCA"]);
        }
    }, [query, pathname, isReady]);

    const onSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const result = getSearchResponseInputSchema.safeParse({
            query: inputValue,
            regulation: RegulationEnum["FCA"],
        });

        if (result.error) {
            console.error("Error in validating data", result.error);
            return;
        }

        push(
            `/search?q=${encodeURIComponent(inputValue)}&regulation=${
                RegulationEnum["FCA"]
            }`,
        );
    };

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);
    };

    return (
        <form
            onSubmit={onSubmit}
            className={clsx(
                "flex py-2 px-4 rounded-lg hover:bg-gray-50 transition duration-150 h-16 text-base bg-white border border-gray-300 focus-within:border-theme-secondary",
                className,
            )}
        >
            <div className="flex self-center w-full h-full">
                <Search className="size-4 fill-gray-800 m-auto" />
                <input
                    placeholder="Search or ask questions"
                    className={
                        "flex-1 px-4 font-light text-base bg-transparent focus-visible:outline-none truncate"
                    }
                    value={inputValue}
                    onChange={handleChange}
                />
            </div>
        </form>
    );
};
