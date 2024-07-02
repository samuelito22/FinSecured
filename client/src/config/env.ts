import * as z from "zod";

const EnvironmentSchema = z.object({
    apiUrl: z.string(),
});

const getValidatedEnvironment = () => {
    const rawEnvironment = {
        apiUrl: process.env.NEXT_PUBLIC_API_URL,
    };

    const validationResult = EnvironmentSchema.safeParse(rawEnvironment);

    if (!validationResult.success) {
        console.error(
            "Failed to parse environment variables:",
            validationResult.error,
        );

        const errorDetails = Object.entries(
            validationResult.error.flatten().fieldErrors,
        )
            .map(([key, errors]) => `- ${key}: ${errors.join(", ")}`)
            .join("\n");

        throw new Error(
            `Invalid environment configuration provided.
The following variables are missing or invalid:
${errorDetails}
`,
        );
    }

    return validationResult.data;
};

export const env = getValidatedEnvironment();
