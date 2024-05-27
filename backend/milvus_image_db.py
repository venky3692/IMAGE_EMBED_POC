from pymilvus import CollectionSchema, FieldSchema, DataType, connections, Collection
from pymilvus import utility

class milvus_image:
    def __init__(self):
        connections.connect(host="localhost", port=19530)
        # data_collection = Collection(name= "IMAGE_EMBEDDINGS")
        # data_collection.drop()
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
            dim = 768
        )

        self.image_name = FieldSchema(
            name = 'image_name',
            dtype= DataType.VARCHAR,
            max_length = 65535
        )

        schema_for_collection = CollectionSchema(
            fields= [self.document_id, self.embeddings, self.image_name],
            enable_dynamic_field = True
        )

        data_collection = Collection(name= "IMAGE_EMBEDDINGS", schema= schema_for_collection, db_name="ABCD" )

        return data_collection

obj = milvus_image()
obj.make_schema_and_collection()
