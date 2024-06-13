import { Request, Response } from "express";
import { CustomApiError, sendErrorResponse, sendSuccessResponse } from "../../../../shared/utils";
import { pgvectorStoreFCA } from "../../../../shared/db/vectorStore.config";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import mistralAIModel from "../../../../shared/db/mistralAI.config";

export const getAnswerToQuery = async (req: Request, res: Response) => {
    const { query } = req.body;

    try {
        // Perform the similarity search
        const similaritySearchResult = await pgvectorStoreFCA.similaritySearchWithScore(query, 5);
        const highestScore = Math.max(...similaritySearchResult.map(doc => doc[1]));

        // Extract and format context from the top document(s)
        const sortedDocuments = similaritySearchResult.sort((a, b) => b[1] - a[1]);
        const context = sortedDocuments.map(doc => `${doc[0].pageContent}`).join(' \n\n');

        // Create a chat prompt including the context and the user query
        const prompt = ChatPromptTemplate.fromMessages([
            ["system", "You are a highly knowledgeable assistant specializing in financial regulations. Your goal is to provide accurate, detailed, and specific answers that help users comply with financial regulations."],
            ["system", "Consider the following information extracted from the most relevant documents to answer the query:"],
            ["system", "{context}"], 
            ["human", "{query}"],
            ["system", "answer according to the language of the user's question."],
            ["system", "When answering, please cite the relevant sections and provide a concise explanation of how they apply to the user's situation. Ensure the information is up-to-date and accurate."]
        ]);
        

        const chain = prompt.pipe(mistralAIModel);
        
        const response = await chain.invoke({
        query,
        context
        });

        let confidenceLevel;

        if (highestScore >= 0.9) {
            confidenceLevel = "high confidence";
        } else if (highestScore >= 0.7 && highestScore < 0.9) {
            confidenceLevel = "moderate confidence";
        } else if (highestScore >= 0.5 && highestScore < 0.7) {
            confidenceLevel = "low confidence";
        } else {
            confidenceLevel = "minimal confidence";
        }
        
        sendSuccessResponse(res, 200, `Query successfully answered with ${confidenceLevel}.`, { answer: response.content, source: sortedDocuments.map((doc) => doc[0].metadata) });


    } catch (error:any) {
        if (error instanceof CustomApiError) {
            sendErrorResponse(res, error.statusCode, error.message, error, 'AnswerToQuery');
        } else {
            console.error('Unexpected error:', error);
            sendErrorResponse(res, 500, 'Internal server error', error, 'AnswerToQuery');
        }
    }
};
