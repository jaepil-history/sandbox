<<<<<<< HEAD
/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 15
 * Time: 오후 2:26
 * To change this template use File | Settings | File Templates.
 */

var mongodb = require('mongodb'),
    server = new mongodb.Server("localhost", 27017, {}),
    sys = require('util'),
    db = new mongodb.Db('test', server, {});

var query={"ts": {$gte: 1000}};
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

//var MR = {
//    mapreduce: "user_info",
//    out:  'resultjs',
//    query: query,
//    map: map.toString(),
//    reduce: reduce.toString(),
//    finalize: finalize.toString()
//};

db.open(function (err, client) {
    if(err) {
        console.log('DB: Failed to connect the database');
    }
    else {
        console.log('DB: Database is connected');

        db.collection('user_info').mapReduce(map, reduce, {
            out: {replace: 'resultjs'},
            query: query,
            finalize: finalize
            }, function (err, collection){
                if(err) {
                    console.log('Map reduce: Fail.');
                }
                else {
                    console.log('Map reduce: Success.');
                    //console.log(stats);
                    console.log(collection);
//                    db.close();
//                    db.on("close", function (err) {
//                        if (err) throw err;
//                        process.exit(0)
//                    });
                }
        });
    }
=======
/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 15
 * Time: 오후 2:26
 * To change this template use File | Settings | File Templates.
 */

var mongodb = require('mongodb'),
    server = new mongodb.Server("localhost", 27017, {}),
    sys = require('util'),
    db = new mongodb.Db('test', server, {});

var query={"ts": {$gte: 1000}};
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

//var MR = {
//    mapreduce: "user_info",
//    out:  'resultjs',
//    query: query,
//    map: map.toString(),
//    reduce: reduce.toString(),
//    finalize: finalize.toString()
//};

db.open(function (err, client) {
    if(err) {
        console.log('DB: Failed to connect the database');
    }
    else {
        console.log('DB: Database is connected');

        db.collection('user_info').mapReduce(map, reduce, {
            out: {replace: 'resultjs'},
            query: query,
            finalize: finalize
            }, function (err, collection){
                if(err) {
                    console.log('Map reduce: Fail.');
                }
                else {
                    console.log('Map reduce: Success.');
                    //console.log(stats);
                    console.log(collection);
//                    db.close();
//                    db.on("close", function (err) {
//                        if (err) throw err;
//                        process.exit(0)
//                    });
                }
        });
    }
>>>>>>> e1fa4f7d9c8eb0592f3156be59486cb533826530
});