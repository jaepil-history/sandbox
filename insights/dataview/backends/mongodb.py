try:
    import pymongo
except ImportError:
    pymongo = None

from dataview.core.exceptions import ImproperlyConfigured
from dataview.core import settings


class MongoBackend():

    # Cron is for testing purposes
    internal_collections = ['cron', 'sessions', 'users']
    #                         '51ada4f8bdeadf2d03d96f25.event.all',
    #                         '51ada4f8bdeadf2d03d96f25.event.apa',
    #                         '51ada4f8bdeadf2d03d96f25.event.cpu',
    #                         '51ada4f8bdeadf2d03d96f25.event.pgr',
    #                         '51ada50ebdeadf2d09f110a9.event.all',
    #                         '51ada50ebdeadf2d09f110a9.event.apa',
    #                         '51ada50ebdeadf2d09f110a9.event.cpu',
    #                         '51ada50ebdeadf2d09f110a9.event.pgr',
    #                         '51ada51cbdeadf2d0f85ee6b.event.all',
    #                         '51ada51cbdeadf2d0f85ee6b.event.apa',
    #                         '51ada51cbdeadf2d0f85ee6b.event.cpu',
    #                         '51ada51cbdeadf2d0f85ee6b.event.pgr',
    #                         '51ada4f8bdeadf2d03d96f25.processed',
    #                         '51ada50ebdeadf2d09f110a9.processed',
    #                         '51ada51cbdeadf2d0f85ee6b.processed'
    #                         ]

    host = settings.MONGO['host']
    port = settings.MONGO['port']
    user = settings.MONGO['user']
    password = settings.MONGO['password']
    database = settings.MONGO['database']
    valid_collections = settings.PROCESSED_LIST + internal_collections

    def __init__(self):
        if not pymongo:
            raise ImproperlyConfigured(
                    "You need to install the pymongo library to use the "
                    "MongoDB backend.")

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

    def get_collection(self, collection):
        db = self.get_database()
        
        if collection in self.valid_collections:
            if collection in self.internal_collections:
                collection = "{0}".format(collection) # protect the collection that dataview uses internally
            else:
                collection = "processed_{0}".format(collection)
            
            collection = db[collection]
        
        else:
            return False

        return collection

    
    def index(self, collection):
        collection = self.get_collection(collection)
        collection.ensure_index([('time', pymongo.DESCENDING)])
    

    def store_entry(self, entry, collection):
        """ Stores a system entry  """
        
        collection = self.get_collection(collection)
        
        if collection:
            collection.save(entry, safe=True)   

    def store_entries(self, entries):
        ''' 
            List with dictionaries, loops through all of them and saves them to the database
            Accepted format:
            {'cpu': {'time': 1313096288, 'idle': 93, 'wait': 0, 'user': 2, 'system': 5}}
        '''
        for key, value in entries.iteritems():
            self.store_entry(value, key)
            self.index(key)

backend = MongoBackend()
