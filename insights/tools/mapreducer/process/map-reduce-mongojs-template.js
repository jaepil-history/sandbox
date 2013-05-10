/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 15
 * Time: 오후 2:00
 * To change this template use File | Settings | File Templates.
 */

//var Integration = new Schema({
//    _mt: String,
//    _dt: Date,
//    uuid: Number,
//    b: String,        // '1936/10/22'
//    g: String,        // gender: {f, m, u} (female, male, unknown)
//    lc: String,       // country
//    f: Number         // friends_count: Number,
//    data: String,
//    timestamp: Number,
//    age: Number,
//    tracking_uid: String,
//    url: String,
//    ip: String
//}, {collection: 'appId.integration'});

var async = require('async');
var moment = require('moment');
var dbclient = require('../dbclient');

var integration_collection = '51776dbc1d41c8061ef024b5.integration';
var stats_reports_collection = 'stats_reports';

var query={"ts": {$gte: 800}};
//query = {"_id.ts":{$gte:12060500,$lte:12060523}};
console.log(query);

var map = function () {
    mkey = {gender: this.g, country: this.lc};
    mval = {count: 1, total: this.f};
    emit (mkey, mval);
};
console.log('map built');

var reduce = function (rkey, rvals) {
    var reducedValue = {count: 0, total: 0};
    for (var i = 0; i < rvals.length; i++) {
        reducedValue.count += rvals[i].count;
        reducedValue.total += rvals[i].total;
    }
    return reducedValue;
};
console.log('reduce built');

var finalize = function(key, reducedValue) {
    reducedValue.average = reducedValue.total / reducedValue.count;
    return reducedValue;
};
console.log('finalize built');

var MR = {
    mapreduce: integration_collection,
    out:  {merge: "resultjs"},
    query: query,
    map: map.toString(),
    reduce: reduce.toString(),
    finalize: finalize.toString(),
    verbose: true
};

dbclient.db_processed.executeDbCommand(MR, function(err, result) {
    if (err) throw err;

    //console.log(dbres);
    var doc = result.documents[0];//.results;
    console.log("executing map reduce with mongojs, results:");
    console.log(JSON.stringify(doc));

    doc.ts = Date.now();
    console.log(JSON.stringify(doc));
    dbclient.db_processed.collection(stats_reports_collection).insert(doc, function(err){
        if (err) throw err;
        console.log('insert completed');
    });
});

//exports.doMapReduce = function(option, callback) {
//
//    dbclient.db_processed.executeDbCommand(MR, function(err, result) {
//        if (err) throw err;
//
//        //console.log(dbres);
//        var doc = result.documents[0];//.results;
//        console.log("executing map reduce with mongojs, results:");
//        console.log(JSON.stringify(doc));
//
//        doc.ts = Date.now();
//        console.log(JSON.stringify(doc));
//        dbclient.db_processed.collection(stats_reports_collection).insert(doc, function(err){
//            if (err) throw err;
//            console.log('insert completed');
//        });
//    });
//
//}

