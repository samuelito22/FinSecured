import localFont from "next/font/local";
import { Rubik, Poppins, DM_Sans } from "next/font/google";

export const broxaFont = localFont({
    src: "../../public/fonts/broxa/Broxa.woff2",
});

export const rubikFont = Rubik({
    subsets: ["latin"],
});

export const dmSansFont = DM_Sans({
    subsets: ["latin"],
});

export const poppinsFont = Poppins({
    weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
    subsets: ["latin"],
});
