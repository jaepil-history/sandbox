from hashlib import sha1
from os import getenv

from pymongo import DESCENDING, ASCENDING

from dataview.backends.mongodb import MongoBackend


class BaseModel(object):
    
    page_size = 50

    def __init__(self):
        self.mongo = MongoBackend()
        
        # Set in the test suite 
        #  os.environ['DATAVIEW_ENV'] = 'test'
        if getenv('DATAVIEW_ENV', None) == 'test':
            self.mongo.database = 'dataview_test'

    def paginate(self, cursor, page=None):
        
        page = 1 if page == None else int(page)
        page = 1 if page == 0 else page
        
        rows = cursor.clone().count()
        total_pages = rows/self.page_size
        total_pages = 1 if total_pages == 0 else total_pages
        
        page = total_pages if page > total_pages else page

        skip = self.page_size * (page - 1)

        result = cursor.limit(self.page_size).skip(skip)

        pagination = {
            "pages": total_pages,
            "current_page": page,
            "result": result
        }
        
        return pagination


class DashboardModel(BaseModel):
    
    def __init__(self):
        super(DashboardModel, self).__init__()

    def get_last_system_check(self, active_system_checks):
        last_check = {}
        
        for check in active_system_checks:
            row = self.mongo.get_collection(check)
            # don't break the dataview if the daemon is stopped
            try:
                last_check[check] = row.find({"last":{"$exists" : False}},limit=1).sort('time', DESCENDING)[0]
            except IndexError:
                last_check[check] = False

        return last_check

    def get_last_process_check(self, active_process_checks):
        process_check = {}

        for check in active_process_checks:
            row = self.mongo.get_collection(check)
            try:
                process_check[check] = row.find({"last":{"$exists" : False}}, limit=1).sort('time', DESCENDING)[0]
            except IndexError:
                process_check[check] = False

        return process_check


class ProcessedDataModel(BaseModel):

    def __init__(self):
        super(ProcessedDataModel, self).__init__()

    """
    Return pymongo object of processed data
    """
    def get_processed_data(self, selected_data, date_from, date_to, group):

        data = {}

        for check in selected_data:
            row = self.mongo.get_collection(check)

            if row is None:
                print 'collection is None'
                try:
                    data[check] = row.find({"_dt": {"$gte": date_from,"$lte": date_to }}).sort('_dt', ASCENDING)
                except IndexError:
                    data[check] = False

        return data

    """
    Used in the Javascript calendar - doesn't permit checks for dates before this date
    """
    def get_first_check_date(self):
        row = self.mongo.get_collection('cpu')
        start_date = row.find_one()

        if start_date != None:
            start_date = start_date.get('time', 0)
        else:
            start_date = 0

        return start_date


class UserModel(BaseModel):
    
    def __init__(self):
        super(UserModel, self).__init__()
        self.collection = self.mongo.get_collection('users')


    def create_user(self, userdata):
        userdata['password'] = sha1(userdata['password']).hexdigest()
        self.collection.save(userdata)

    def check_user(self, userdata):
        userdata['password'] = sha1(userdata['password']).hexdigest()
        result = self.collection.find_one({"username": userdata['username'],
                                    "password": userdata['password']})


        return result if result else {}

    def update_password(self, userdata, new_password):
        new_password = sha1(new_password).hexdigest()
        self.collection.update({"username": userdata['username']},
                {"$set": {"password": new_password}})

    
    def count_users(self):
         return self.collection.count() 

    def username_exists(self, username):
        result = self.collection.find({"username": username}).count()

        return result


processed_data_model = ProcessedDataModel()
dashboard_model = DashboardModel()
user_model = UserModel()