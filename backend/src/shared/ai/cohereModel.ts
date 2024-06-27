import { Cohere, CohereEmbeddings } from "@langchain/cohere";
import { config } from "../config";
import { CohereRerank } from "@langchain/cohere";

const cohereChat = new Cohere({
  apiKey: config.cohereApiKey.apiKey 
});

const cohereRerank = new CohereRerank({
    apiKey: config.cohereApiKey.apiKey , // Default
    model: "rerank-english-v2.0", // Default
  });


const cohereEmbeddings = new CohereEmbeddings({
apiKey: config.cohereApiKey.apiKey
});

export {cohereChat, cohereRerank, cohereEmbeddings};