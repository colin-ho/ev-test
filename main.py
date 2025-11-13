# import daft
# from daft.functions import regexp_extract
# from daft.functions.ai import embed_text
# from daft.io import S3Config, IOConfig
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# import time
# import os
# from dotenv import load_dotenv

# load_dotenv()

# CHUNK_SIZE = 2048
# CHUNK_OVERLAP = 200

# regex = r"([0-9a-fA-F-]{36})"

# chunk_type = daft.DataType.struct(
#     {
#         "chunk": daft.DataType.string(),
#         "chunk_id": daft.DataType.int64(),
#     }
# )

# io_config = IOConfig(
#     s3=S3Config(
#         key_id=os.environ["AWS_ACCESS_KEY_ID"],
#         access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
#     )
# )

# daft.context.set_planning_config(default_io_config=io_config)

# supabase_connection = os.environ["SUPABASE_CONNECTION"]

# PROVIDER = "openai"

# @daft.func(return_dtype=chunk_type, unnest=True)
# def chunk(text: str):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=CHUNK_SIZE,
#         chunk_overlap=CHUNK_OVERLAP,
#     )
#     for chunk_index, chunk_text in enumerate(splitter.split_text(text)):
#         yield {
#             "chunk": chunk_text,
#             "chunk_id": chunk_index,
#         }


# def embed_with_provider(df: daft.DataFrame) -> daft.DataFrame:
#     provider = PROVIDER
#     if PROVIDER == "transformers":
#         model = "sentence-transformers/all-MiniLM-L6-v2"
#     else:
#         model = "text-embedding-3-small"

#     return df.with_column(
#         "embedding",
#         embed_text(
#             df["chunk"],
#             model=model,
#             provider=provider,
#         ),
#     )


# def embed(source: str, table: str):
#     df = daft.read_parquet(source)
#     df = df.limit(100)

#     df = df.with_column(
#         "candidate_id", regexp_extract(df["path"], r"([0-9a-fA-F-]{36})")
#     )
#     df = df.select("*", chunk(df["decoded_resume"]))

#     df = embed_with_provider(df)
#     df = df.where(daft.col("chunk").not_null())

#     df = df.select("path", "candidate_id", "chunk", "embedding", "chunk_id")
#     df = df.with_column("id", df["candidate_id"] + "-" + df["chunk_id"])

#     print(f"writing to table: {table}")

#     catalog = daft.Catalog.from_postgres(supabase_connection)
#     table = catalog.create_table_if_not_exists(table, df.schema())
#     table.append(df)

#     return {
#         "table": table, 
#     }


# if __name__ == "__main__":
#     embed(
#         source="s3://eventual-candidates-resumes/extracted-text-test-2",
#         table=f"resume_embeddings_{PROVIDER}"
#     )

print("Hello, World!")