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
//}, {collection: 'integration'}); // 마지막은 collection name. 없으면 model_name = collection_name

//var sys = require('util');
var mongodb = require('mongodb');
var server_insight = new mongodb.Server("localhost", 27017, {});
var server_appspand = new mongodb.Server("localhost", 27017, {});
var server_processed = new mongodb.Server("localhost", 27017, {});

var db_insight = new mongodb.Db('test', server_insight, {w:1});
console.log('Connected to DB insight');
var db_appspand = new mongodb.Db('appspand', server_appspand, {w:1});
console.log('Connected to DB appspand');
var db_processed = new mongodb.Db('processed', server_processed, {w:1});
console.log('Connected to DB processed');

var cpu_collection_name = '51776dbc1d41c8061ef024b5.event.cpu';
var uuid;
var cpu_uuid = function(collection_name, uuid) {
    return db_insight.collection(collection_name).findOne({uuid : uuid});
}

var doc;
var all_cursor = db_insight.collection('51776dbc1d41c8061ef024b5.event.all').find();

console.log(all_cursor);

//while(all_cursor.hasNext()) {
//    doc = all_cursor.next();
//    if(doc.get("uuid") != null) uuid = doc.uuid;
//    else continue;
//
//    var user_info = cpu_uuid(cpu_collection_name, uuid);
//    doc.b = user_info.b;
//    doc.g = user_info.g;
//    doc.f = user_info.f;
//
//    db_processed.collection('integration').insert(doc);
//}





