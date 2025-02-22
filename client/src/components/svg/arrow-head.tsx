import { JSX } from "react";

interface ArrowHeadProps {
    className?: string;
}

export const ArrowHead = ({ className }: ArrowHeadProps): JSX.Element => {
    return (
        <svg
            className={className}
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            width="512"
            height="512"
        >
            <g id="_01_align_center" data-name="01 align center">
                <path d="M12,15.5a1.993,1.993,0,0,1-1.414-.585L5.293,9.621,6.707,8.207,12,13.5l5.293-5.293,1.414,1.414-5.293,5.293A1.993,1.993,0,0,1,12,15.5Z" />
            </g>
        </svg>
    );
};
