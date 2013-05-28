<<<<<<< HEAD
/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 15
 * Time: 오후 2:26
 * To change this template use File | Settings | File Templates.
 */

var db_processed_url = 'localhost:27017/test';
var integration_collection = 'user_info';
var out_collection = 'resultjs';
var stats_reports_collection = 'stats_reports';
var collections_processed = [integration_collection, out_collection, stats_reports_collection];
var db_processed = require('mongojs').connect(db_processed_url, collections_processed);

var query={"ts": {$gte: 850}};
//query = {"_id.ts":{$gte:12060500,$lte:12060523}};
console.log(query);

var map = function () {
    mkey = {gender: this.gender, country: this.country};
    mval = {count: 1, total: this.purchase};
    emit (mkey, mval);
};
console.log('map built');

var reduce = function (rkey,rvals) {
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
    out:  {merge: out_collection},
    query: query,
    map: map.toString(),
    reduce: reduce.toString(),
    finalize: finalize.toString(),
    verbose: true
};

db_processed.executeDbCommand(MR, function(err, result) {
    if (err) throw err;

    //console.log(dbres);
    var doc = result.documents[0];//.results;
    console.log("executing map reduce with mongojs, results:");
    console.log(JSON.stringify(doc));

    doc.ts = Date.now();

    console.log(JSON.stringify(doc));
    db_processed.collection(stats_reports_collection).insert(doc, function(err){
        if (err) throw err;
        console.log('insert completed');
    });
});
=======
/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 15
 * Time: 오후 2:26
 * To change this template use File | Settings | File Templates.
 */

var db_processed_url = 'localhost:27017/test';
var integration_collection = 'user_info';
var out_collection = 'resultjs';
var stats_reports_collection = 'stats_reports';
var collections_processed = [integration_collection, out_collection, stats_reports_collection];
var db_processed = require('mongojs').connect(db_processed_url, collections_processed);

var query={"ts": {$gte: 850}};
//query = {"_id.ts":{$gte:12060500,$lte:12060523}};
console.log(query);

var map = function () {
    mkey = {gender: this.gender, country: this.country};
    mval = {count: 1, total: this.purchase};
    emit (mkey, mval);
};
console.log('map built');

var reduce = function (rkey,rvals) {
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
    out:  {merge: out_collection},
    query: query,
    map: map.toString(),
    reduce: reduce.toString(),
    finalize: finalize.toString(),
    verbose: true
};

db_processed.executeDbCommand(MR, function(err, result) {
    if (err) throw err;

    //console.log(dbres);
    var doc = result.documents[0];//.results;
    console.log("executing map reduce with mongojs, results:");
    console.log(JSON.stringify(doc));

    doc.ts = Date.now();

    console.log(JSON.stringify(doc));
    db_processed.collection(stats_reports_collection).insert(doc, function(err){
        if (err) throw err;
        console.log('insert completed');
    });
});
>>>>>>> e1fa4f7d9c8eb0592f3156be59486cb533826530
