import React from "react";

import { MainLayout } from "@components/layout";
import { SearchInput } from "@features/rag-search/components";
import clsx from "clsx";
import { rubikFont } from "@config/fonts";
import { Search } from "@components/svg";
import Link from "next/link";
import { RegulationEnum } from "@customTypes/api";

const SearchAlternatives = [
    "What are the latest FCA regulations on crypto assets?",
    "How do FCA rules apply to the marketing of investment products?",
    "What are the FCA's requirements for anti-money laundering compliance?",
    "Can you explain the FCA guidelines on consumer credit?",
    "What does the FCA say about the use of technology in compliance monitoring?",
];

const Home: React.FC = () => {
    return (
        <MainLayout>
            <section className="container mx-auto py-8 px-5">
                <div className="flex flex-col items-center max-w-2xl m-auto">
                    <div className="text-center text-black">
                        <h1
                            className={clsx(
                                rubikFont.className,
                                "text-[32px] leading-[38px] font-semibold",
                            )}
                        >
                            Navigate complex regulations with ease
                        </h1>
                        <p className={"font-normal text-base mt-5"}>
                            The #1 search engine curated for Financial
                            Compliance
                        </p>
                    </div>
                    <div className="w-full mt-12">
                        <SearchInput />
                    </div>
                    <div className="mt-12 px-4 w-full">
                        <h5 className="text-sm">
                            Try asking or searching for:
                        </h5>
                        <ul>
                            {SearchAlternatives.map((text, idx) => {
                                return (
                                    <li
                                        key={idx}
                                        className="w-full mt-2 flex flex-row hover:cursor-pointer"
                                    >
                                        <Link
                                            href={`/search?q=${encodeURIComponent(
                                                text,
                                            )}&regulation=${
                                                RegulationEnum.FCA
                                            }`}
                                            className="flex flex-row w-full"
                                        >
                                            <Search className="size-[13px] fill-gray-800 self-center" />
                                            <span className="text-[15px] text-theme-secondary hover:underline flex-1 pl-3">
                                                {text}
                                            </span>
                                        </Link>
                                    </li>
                                );
                            })}
                        </ul>
                    </div>
                </div>
            </section>
        </MainLayout>
    );
};

export default Home;
