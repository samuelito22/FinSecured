import { JSX } from "react";

interface TrafficConeProps {
    className?: string;
}

export const TrafficCone = ({ className }: TrafficConeProps): JSX.Element => {
    return (
        <svg
            className={className}
            xmlns="http://www.w3.org/2000/svg"
            id="Layer_1"
            data-name="Layer 1"
            viewBox="0 0 24 24"
        >
            <path d="m6.328,11h11.201l1.581,4H4.691l1.637-4Zm10.41-2L13.18,0h-2.351l-3.683,9h9.592Zm3.163,8H3.872l-2.046,5H0v2h24v-2h-2.123l-1.977-5Z" />
        </svg>
    );
};
