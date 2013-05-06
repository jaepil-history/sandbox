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

var MR = {
    mapreduce: "user_info",
    out:  'resultjs',
    query: query,
    map: map.toString(),
    reduce: reduce.toString(),
    finalize: finalize.toString()
};

db_processed.executeDbCommand(MR, function(err, dbres) {
        if (err) throw err;

        //console.log(dbres);
        var results = dbres.documents[0];//.results;
        console.log("executing map reduce with mongojs, results:");
        console.log(JSON.stringify(results));

//        db.close();
//        db.on("close", function (err) {
//            if (err) throw err;
//            process.exit(0)
//        });
    });
