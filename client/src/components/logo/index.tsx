import { JSX } from "react";
import clsx from "clsx";
import { broxaFont } from "@config/fonts";

interface LogoProps {
    size?: string;
}

const Logo = ({ size = "1em" }: LogoProps): JSX.Element => {
    return (
        <div style={{ fontSize: size }}>
            <span
                className={clsx(broxaFont.className, "font-normal")}
                style={{ marginRight: "0.25em" }}
            >
                FinSecured
            </span>
            {/*
            <div style={{ width: '1em', height: '1em', display: 'inline-block', verticalAlign: 'middle'}} className='text-[#4c2154]'>
                <Image 
                    src={octopus}
                    quality={100}
                    alt='Logo of FinSecured'
                    layout="responsive"
                    width={"100"}
                    height={"100"}
                    color='white'
                />
            </div>
            */}
        </div>
    );
};

export default Logo;
