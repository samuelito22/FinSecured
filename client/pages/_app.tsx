import store from "@redux/store";
import "@styles/global.css";
import { AppProps } from "next/app";
import {
    QueryClient,
    QueryClientProvider,
    HydrationBoundary,
} from "@tanstack/react-query";
import { Provider } from "react-redux";
import "tailwindcss/tailwind.css";

function MyApp({ Component, pageProps }: AppProps): JSX.Element {
    const queryClient = new QueryClient();
    return (
        <QueryClientProvider client={queryClient}>
            <HydrationBoundary state={pageProps.dehydratedState}>
                <Provider store={store}>
                    <Component {...pageProps} />
                </Provider>
            </HydrationBoundary>
        </QueryClientProvider>
    );
}

export default MyApp;
