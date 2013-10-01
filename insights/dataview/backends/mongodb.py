try:
    import pymongo
except ImportError:
    pymongo = None

from dataview.config import settings


class MongoBackend():

    # Cron is for testing purposes
    internal_collections = ['cron', 'sessions', 'users']

    host = settings.MONGO['host']
    port = settings.MONGO['port']
    user = settings.MONGO['user']
    password = settings.MONGO['password']
    database = settings.MONGO['database']
    valid_collections = internal_collections
    for item in settings.PROCESSED_LIST:
        valid_collections.append(item.lower())

    def __init__(self):
        self._database = None
        self._connection = None

    def get_connection(self):
        """Connect to the MongoDB server."""
        from pymongo.connection import Connection
        
        if self._connection is None:
            self._connection = Connection(self.host, self.port)
            return self._connection


    def get_database(self):
        """"Get database from MongoDB connection. """
        if self._database is None:
            conn = self.get_connection()
            db = conn[self.database]
            self._database = db

        return self._database   


    def get_collection(self, collection_name, app_id=None):
        db = self.get_database()
        collection_name = collection_name.lower()

        if collection_name is None:
            raise Exception("Collection name is not specified")

        if collection_name in self.valid_collections:
            if app_id is None:
                if collection_name in self.internal_collections:
                    collection = "{0}".format(collection_name)  # protect the collection that dataview uses internally
                else:
                    return False
            else:
                if not isinstance(app_id, basestring):
                    app_id = str(app_id)

                collection_name_items = [app_id, collection_name]
                collection = ".".join(collection_name_items)

            print 'collection_name: ' + collection
            collection = db[collection]
        
        else:
            return False

        return collection


    def find_from_processed(self, app_id, collection_name, query=None):
        collection = self.get_collection(collection_name, app_id)
        cursor = collection.find(query)
        return cursor


    #def index(self, collection):
    #    collection = self.get_collection(collection)
    #    collection.ensure_index([('time', pymongo.DESCENDING)])
    #
    #def store_entry(self, entry, collection):
    #    """ Stores a system entry  """
    #
    #    collection = self.get_collection(collection)
    #
    #    if collection:
    #        collection.save(entry, safe=True)
    #
    #def store_entries(self, entries):
    #    '''
    #        List with dictionaries, loops through all of them and saves them to the database
    #        Accepted format:
    #        {'cpu': {'time': 1313096288, 'idle': 93, 'wait': 0, 'user': 2, 'system': 5}}
    #    '''
    #    for key, value in entries.iteritems():
    #        self.store_entry(value, key)
    #        self.index(key)

backend = MongoBackend()
