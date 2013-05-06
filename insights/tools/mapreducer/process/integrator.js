/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 11
 * Time: 오후 9:11
 * To change this template use File | Settings | File Templates.
 */

//var Integration = new Schema({
//    _mt: String,
//    _dt: Date,
//    user_uid: Number,
//    birthday: String,
//    gender: String,
//    country: String,
//    friends_count: Number,
//    data: String,
//    timestamp: Number,
//    age: { type: Number, min: 8, max: 75 },
//    tracking_uid: String,
//    url: String,
//    ip: String
//}, {collection: 'integration'});

var db_insight_url = "localhost:27017/test"; // "username:password@example.com/mydb"
var cpu_collection = '51776dbc1d41c8061ef024b5.event.cpu';
var all_collection = '51776dbc1d41c8061ef024b5.event.all';
var collections_insight = [cpu_collection, all_collection];
var db_user_info = require("mongojs").connect(db_insight_url, collections_insight);

var db_appspand_url = 'localhost:27017/appspand';
var application_collection = 'application';
var account_collection = 'account';
var collections_appspand = [application_collection, account_collection];
var db_appspand = require('mongojs').connect(db_appspand_url, collections_appspand);

var db_processed_url = 'localhost:27017/processed';
var integration_collection = 'integration';
var collections_processed = [integration_collection];
var db_processed = require('mongojs').connect(db_processed_url, collections_processed);

db_user_info.collection(all_collection).find({}, function(err, docs) {
    if(err) throw err;
    if(!docs) console.log('No docs found');
    else docs.forEach(function(doc) {
        if(doc.uuid) {
            db_user_info.collection(cpu_collection).findOne({'uuid': doc.uuid}, function(err, cpu) {
                if (err) throw err;
                //console.log(cpu);
                doc['b'] = cpu.b;
                doc['g'] = cpu.g;
                doc['f'] = cpu.f;
                db_processed.collection('integration').insert(doc, function (err, inserted) {
                    if (err) throw err;
                    console.log(inserted);
                });
            });
        }
        else
            db_processed.collection('integration').insert(doc, function (err, inserted) {
                if (err) throw err;
                console.log(inserted);
            });
    });
});




