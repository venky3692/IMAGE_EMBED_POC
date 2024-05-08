from pymilvus import CollectionSchema, FieldSchema, DataType, connections, Collection
from pymilvus import utility

class milvus:
    def __init__(self):
        connections.connect(host="localhost", port=19530)
        print('connected')

    def make_schema_and_collection(self):
        self.document_id = FieldSchema(
            name = 'image_id',
            dtype=DataType .INT64,
            is_primary = True,
            auto_id = True
        )

        self.embeddings = FieldSchema(
            name= 'embeddings', 
            dtype = DataType.FLOAT_VECTOR,
            dim = 1024
        )

        self.image_name = FieldSchema(
            name = 'image_name',
            dtype= DataType.VARCHAR
        )

        schema_for_collection = CollectionSchema(
            fields= [self.document_id, self.metadata, self.embeddings, self.image_name],
            enable_dynamic_field = True
        )

        data_collection = Collection(name= "IMAGE_EMBEDDINGS", schema= schema_for_collection, db_name="ABCD" )

        return data_collection

obj = milvus()
