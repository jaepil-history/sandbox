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
var collections_processed = [integration_collection];
var db_processed = require('mongojs').connect(db_processed_url, collections_processed);

//var mr = {};
//
//mr.query = {"ts": {$gte: 900}};
//console.log(mr.query);
//
//mr.map = function () {
//    var mkey = {gender: this.gender, country: this.country};
//    var mval = {count: 1, total: this.purchase};
//    emit (mkey, mval);
//};
//
//mr.reduce = function (rkey,rvals) {
//    var reducedValue = {count: 0, total: 0};
//    for (var i = 0; i < rvals.length; i++) {
//        reducedValue.count += rvals[i].count;
//        reducedValue.total += rvals[i].total;
//    }
//    return reducedValue;
//};
//
//mr.finalize = function(key, reducedValue) {
//    reducedValue.average = reducedValue.total / reducedValue.count;
//    return reducedValue;
//};
//
//mr.out = {merge: "resultjs"};
//mr.verbose = true;

var query={"ts": {$gte: 700}};
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

var option = {
    out:  {merge: "resultjs"},
    query: query,
    finalize: finalize.toString()
};

var result = {};// = new StatsReport();
result.timestamp = Date.now();

console.log(db_processed.collection('user_info'));

db_processed.collection('user_info').mapReduce(map.toString(), reduce.toString(), option, function (err, results) {
    if (err) {
        console.log(err);
    }
    else {
        console.log('m/r completed');
        console.log(results);

//        result.processtime = stats.processtime;
//        result.counts = stats.counts;
//        result.timing = stats.timing;
//
//        result.save(function (err) {
//            if (err) throw err;
//            console.log('stats is saved...');
//        })
    }
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
var collections_processed = [integration_collection];
var db_processed = require('mongojs').connect(db_processed_url, collections_processed);

//var mr = {};
//
//mr.query = {"ts": {$gte: 900}};
//console.log(mr.query);
//
//mr.map = function () {
//    var mkey = {gender: this.gender, country: this.country};
//    var mval = {count: 1, total: this.purchase};
//    emit (mkey, mval);
//};
//
//mr.reduce = function (rkey,rvals) {
//    var reducedValue = {count: 0, total: 0};
//    for (var i = 0; i < rvals.length; i++) {
//        reducedValue.count += rvals[i].count;
//        reducedValue.total += rvals[i].total;
//    }
//    return reducedValue;
//};
//
//mr.finalize = function(key, reducedValue) {
//    reducedValue.average = reducedValue.total / reducedValue.count;
//    return reducedValue;
//};
//
//mr.out = {merge: "resultjs"};
//mr.verbose = true;

var query={"ts": {$gte: 700}};
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

var option = {
    out:  {merge: "resultjs"},
    query: query,
    finalize: finalize.toString()
};

var result = {};// = new StatsReport();
result.timestamp = Date.now();

console.log(db_processed.collection('user_info'));

db_processed.collection('user_info').mapReduce(map.toString(), reduce.toString(), option, function (err, results) {
    if (err) {
        console.log(err);
    }
    else {
        console.log('m/r completed');
        console.log(results);

//        result.processtime = stats.processtime;
//        result.counts = stats.counts;
//        result.timing = stats.timing;
//
//        result.save(function (err) {
//            if (err) throw err;
//            console.log('stats is saved...');
//        })
    }
>>>>>>> e1fa4f7d9c8eb0592f3156be59486cb533826530
});