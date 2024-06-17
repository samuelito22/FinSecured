import { Cohere } from "@langchain/cohere";
import { config } from "../config";

const cohereAIModel = new Cohere({
  maxTokens: 150,
  apiKey: config.cohereApiKey.apiKey // In Node.js defaults to process.env.COHERE_API_KEY
});

export default cohereAIModel;