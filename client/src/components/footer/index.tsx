import { JSX } from "react";

export const Footer = (): JSX.Element => {
    return (
        <footer className={"bg-theme-tertiary py-7 px-4 md:px-20"}>
            <div className="container mx-auto w-full">
                <span className="text-gray-500 text-sm">
                    Copyright © 2024 - All right reserved by FinSecured
                </span>
            </div>
        </footer>
    );
};
