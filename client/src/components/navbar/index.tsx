import Logo from "@components/logo";
import { JSX } from "react";

export const Navbar = (): JSX.Element => {
    return (
        <div className="py-2 px-4 border-b border-b-gray-200">
            <div className="max-w-[210px] pl-4">
                <Logo size="1.2em" />
            </div>
        </div>
    );
};
