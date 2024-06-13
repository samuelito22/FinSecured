import { ChatMistralAI } from "@langchain/mistralai";
import { config } from "../config";

const mistralAIModel = new ChatMistralAI({
  apiKey: config.mistral_ai.apiKey,
  model: "mistral-small",
  maxTokens: 200
});

export default mistralAIModel;