import {
    PGVectorStore,
  } from "@langchain/community/vectorstores/pgvector";
import pg from 'pg';
import { config } from "../config";
import { cohereEmbeddings } from "../ai/cohereModel";

const { Pool } = pg;

const reusablePool = new Pool({
    connectionString: config.database.embeddingDatabaseUrl
  });

const configEmbeddingFCA = {
    pool: reusablePool,
    tableName: "langchain_pg_embedding",
    collectionName: "fca_embeddings",
    collectionTableName: "langchain_pg_collection",
    columns: {
      idColumnName: "id",
      vectorColumnName: "embedding",
      contentColumnName: "document",
      metadataColumnName: "cmetadata",
    },
  };


const pgvectorStoreFCA = new PGVectorStore(cohereEmbeddings, configEmbeddingFCA);

const closeOpenPools = async () => {
    if(reusablePool){
        await reusablePool.end()
    }
}

/**
 * prompt = f"""
Context information is below.
---------------------
{retrieved_chunk}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: {question}
Answer:
"""
 */

export { pgvectorStoreFCA, closeOpenPools }