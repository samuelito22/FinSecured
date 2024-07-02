import clsx from "clsx";
import React from "react";

interface SearchAnswersProps {
    isLoading: boolean;
    answer?: string;
    className?: string;
}

const SkeletonLoading = () => {
    const backgroundColor = "bg-gray-200";

    return (
        <div className="animate-pulse flex flex-col space-y-4">
            <div className="flex flex-col space-y-2 w-full">
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
                    className={clsx(backgroundColor, "h-3 w-4/5 rounded")}
                ></div>
            </div>
            <div className={clsx(backgroundColor, "h-3 w-64 rounded")}></div>
        </div>
    );
};

interface FormattedAnswerProps {
    answer: string;
}

const FormattedAnswer: React.FC<FormattedAnswerProps> = ({ answer }) => {
    const regex = /\[\d+\]/g;

    const formatText = (text: string) => {
        const parts = text.split(regex);
        const matches = text.match(regex);

        return parts.flatMap((part, index) => [
            part,
            matches && matches[index] ? (
                <sup key={index} className="text-theme-secondary text-xs">
                    {matches[index]}
                </sup>
            ) : null,
        ]);
    };

    return (
        <p className="text-[0.95rem] leading-6 hover:underline decoration-dashed cursor-pointer underline-offset-4 decoration-1 decoration-theme-gray text-gray-900">
            {formatText(answer)}
        </p>
    );
};

export const SearchAnswers: React.FC<SearchAnswersProps> = ({
    isLoading,
    answer,
    className,
}) => {
    return (
        <div className={clsx("w-full", className)}>
            {isLoading ? (
                <SkeletonLoading />
            ) : answer ? (
                <FormattedAnswer answer={answer} />
            ) : null}
        </div>
    );
};
