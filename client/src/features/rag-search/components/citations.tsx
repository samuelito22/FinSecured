import { ArrowHead } from "@components/svg";
import { Citation } from "@customTypes/api";
import clsx from "clsx";
import Link from "next/link";
import { JSX, useState } from "react";

interface CitationProps {
    data?: Citation[];
    className?: string;
    isLoading: boolean;
}

interface CitationBlockProps {
    citation: Citation;
}

const CitationBlock = ({ citation }: CitationBlockProps): JSX.Element => {
    const [toggle, setToggle] = useState(false);

    const handleToggle = () => {
        setToggle((prevState) => {
            return !prevState;
        });
    };

    return (
        <div className={"w-full flex flex-col"}>
            <div className="flex items-center justify-between self-center w-full">
                <Link
                    href={citation.file_url}
                    target="_blank"
                    className="text-theme-secondary text-[15px]"
                >
                    Citation No. {citation.id}
                </Link>
                <div
                    onClick={handleToggle}
                    className="size-8 cursor-pointer hover:bg-gray-200 transition-all duration-150 rounded-md flex justify-center items-center ease-in-out"
                >
                    <ArrowHead
                        className={clsx(
                            "size-5 object-contain fill-gray-600 transition-all duration-300",
                            toggle ? "rotate-180" : "rotate-0",
                        )}
                    />
                </div>
            </div>
            <div
                className={clsx(
                    "transition-max-height duration-150 overflow-hidden ease-in-out flex flex-col space-y-2",
                    toggle ? "max-h-[1000px]" : "max-h-0",
                )}
            >
                {citation.quotes.map((field, idx) => {
                    return (
                        <q
                            key={idx}
                            className="font-light text-sm text-gray-600"
                        >
                            {field}
                        </q>
                    );
                })}
            </div>
        </div>
    );
};

const SkeletonLoading = () => {
    const backgroundColor = "bg-gray-200";

    return (
        <div className="animate-pulse flex flex-col space-y-4">
            <div className="flex flex-col space-y-2 w-full">
                <div
                    className={clsx(
                        backgroundColor,
                        "h-5 max-w-56 w-full rounded",
                    )}
                ></div>
                <div
                    className={clsx(backgroundColor, "h-3 w-full rounded")}
                ></div>
                <div
                    className={clsx(backgroundColor, "h-3 w-full rounded")}
                ></div>
                <div
                    className={clsx(backgroundColor, "h-3 w-full rounded")}
                ></div>
                <div
                    className={clsx(backgroundColor, "h-3 w-full rounded")}
                ></div>
            </div>
        </div>
    );
};

export const Citations = ({
    className,
    data,
    isLoading,
}: CitationProps): JSX.Element => {
    return (
        <div className={clsx("w-full", className)}>
            {isLoading ? (
                <SkeletonLoading />
            ) : data ? (
                <>
                    <span className="text-sm font-medium">
                        Cited Articles:{" "}
                    </span>
                    <div className="flex flex-col space-y-1">
                        {data?.map((field, idx) => (
                            <CitationBlock key={idx} citation={field} />
                        ))}
                        {data.length === 0 && (
                            <span className="font-light text-sm">
                                No citations found for this search.
                            </span>
                        )}
                    </div>
                </>
            ) : null}
        </div>
    );
};
