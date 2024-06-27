import { Request, Response } from "express";
import { CustomApiError, sendErrorResponse, sendSuccessResponse } from "../../../../shared/utils";
import { pgvectorStoreFCA } from "../../../../shared/db/vectorStore.config";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { Document } from "@langchain/core/documents";
import { cohereChat, cohereRerank } from "../../../../shared/ai/cohereModel";

const docsIsEmpty = (res: Response) => {
    return sendSuccessResponse(res, 200, `Query successfully answered.`, { answer: "We could not find reliable information for your query. For accurate and safe advice, please consult a compliance expert or refine your inquiry." });
}

export const getAnswerToQuery = async (req: Request, res: Response) => {
    const { query } = req.body;

    try {
        const similaritySearchResult = await pgvectorStoreFCA.similaritySearch(query);
        console.log(JSON.stringify(similaritySearchResult, null, 2));
        

        const prompt = ChatPromptTemplate.fromMessages([
            ["system", "You are a sophisticated AI specializing in financial regulations. Your primary objective is to provide precise, comprehensive, and specific information that assists users in adhering to financial regulations."],
            ["system", "Based on the extracted information from highly relevant documents, consider the following context for formulating your response:"],
            ["system", "{context}"], // dynamically inserted context from relevant documents
            ["human", "{query}"], // dynamically inserted user query
            ["system", "Craft your response to mirror the user's language style. Provide detailed answers that directly address the user's query."],
            ["system", "Your answer should cite specific sections of the relevant laws or guidelines and explain their implications for the user's specific situation. Make sure all information is current and accurately reflects the latest regulatory standards."],
            ["system", "Conclude your response with a definitive statement. Avoid ending with questions, and aim for concise yet comprehensive replies."]
        ]);
        

        const chain = prompt.pipe(cohereChat);
       
        return sendSuccessResponse(res, 200, `Query successfully answered.`, { answer: "" });


    } catch (error:any) {
        if (error instanceof CustomApiError) {
            sendErrorResponse(res, error.statusCode, error.message, error, 'AnswerToQuery');
        } else {
            console.error('Unexpected error:', error);
            sendErrorResponse(res, 500, 'Internal server error', error, 'AnswerToQuery');
        }
    }
};

