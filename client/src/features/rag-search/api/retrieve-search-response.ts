import { UseMutationResult, useMutation } from "@tanstack/react-query";
import { z } from "zod";

import { api } from "@lib/api-client";
import { MutationConfig } from "@lib/react-query";
import { RagSearchAnswer, RegulationEnum } from "@customTypes/api";

export const getSearchResponseInputSchema = z.object({
    regulation: z.nativeEnum(RegulationEnum),
    query: z.string().min(1, "Required"),
});

export type GetSearchResponseInput = z.infer<
    typeof getSearchResponseInputSchema
>;

export const getSearchResponse = ({
    data,
}: {
    data: GetSearchResponseInput;
}): Promise<RagSearchAnswer> => {
    return api.post(`api/v1/documents/answer`, data);
};

type UseSearchResponseOptions = {
    mutationConfig?: MutationConfig<typeof getSearchResponse>;
};

export const useSearchResponse = ({
    mutationConfig,
}: UseSearchResponseOptions = {}): UseMutationResult<
    RagSearchAnswer,
    Error,
    { data: GetSearchResponseInput },
    unknown
> => {
    const { ...restConfig } = mutationConfig || {};

    return useMutation({
        ...restConfig,
        mutationFn: getSearchResponse,
    });
};
