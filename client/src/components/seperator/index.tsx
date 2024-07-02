import clsx from "clsx";
import { JSX } from "react";

interface SeperatorProps {
    className?: string;
}

export const Seperator = ({ className }: SeperatorProps): JSX.Element => {
    return <div className={clsx("h-[0.8px] w-full bg-zinc-200", className)} />;
};
