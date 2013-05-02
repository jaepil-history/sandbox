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
var BSON = require('mongodb').pure().BSON;
var server1 = new mongodb.Server("localhost", 27017, {});
var server2 = new mongodb.Server("localhost", 27017, {});

var db_user_info = new mongodb.Db('test', server1, {w:1});
console.log('Connected to DB test');
//var db_appspand = new mongodb.Db('appspand', server, {w:1});
//console.log('Connected to DB appspand');
var db_processed = new mongodb.Db('processed', server2, {w:1});
console.log('Connected to DB processed');

//var cpu_collection_name = 'user_info';
//
//var uuid;
//var cpu_uuid = function(collection_name, uuid) {
//    return db_insight.collection(collection_name).findOne({uuid : uuid});
//}

//db_user_info.open(function(err, db) {
//    db.collection('user_info', function(err, collection) {
//        collection.find({}, function(err, cursor) {
//            cursor.toArray(function(err, docs) {
//                console.log("Found " + docs.length + " documents");
//                var queryResults = [];
//                for(var i=0; i<docs.length; i++) {
//                    queryResults[queryResults.length] = docs[i];
//                }
//                db_user_info.close();
//            });
//        });
//    });
//});

db_user_info.open(function(err, db_user_info) {
    db_processed.open(function(err,db_processed) {
        var doc;
        db_user_info.collection('user_info', function(err, collection) {
            collection.find({}, function(err, cursor) {
                cursor.toArray(function(err, docs) {
                    for(var i = 0; i < docs.length; i++) {
                        doc = docs[i];
                        if(doc.uuid != none) uuid = doc.uuid;
                        else continue;

                        doc.b = 1;
                        doc.g = 2;
                        doc.f = 3;

                        db_processed.collection('integration').insert(doc);
                    }
                });
            })
        });
    });
});






