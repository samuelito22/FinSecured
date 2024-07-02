import { Footer } from "@components/footer";
import { dmSansFont } from "@config/fonts";
import clsx from "clsx";
import { JSX } from "react";

export const MainLayout = ({
    children,
}: {
    children: React.ReactNode;
}): JSX.Element => {
    return (
        <div className="flex flex-col min-h-screen">
            <main className={clsx(dmSansFont.className, "flex flex-grow ")}>
                {children}
            </main>
            <Footer />
        </div>
    );
};
