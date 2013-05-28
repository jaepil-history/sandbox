/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 15
 * Time: 오후 2:00
 * To change this template use File | Settings | File Templates.
 */

var mongoose = require('mongoose');

// db 연결
mongoose.connect('mongodb://localhost/test');
var db = mongoose.connection;
console.log('Connected to DB test');

console.log('BEGIN');
// query 정의
var query={"ts": {$gte: 1000}};
console.log(query);

// map 정의
var map = function () {
    var mkey = {gender: this.gender, country: this.country};
    var mval = {count: 1, total: this.purchase};
    emit (mkey, mval);
};
console.log('map built');

// reduce 정의
var reduce = function (rkey,rvals) {
    var reducedValue = {count: 0, total: 0};
    for (var i = 0; i < rvals.length; i++) {
       reducedValue.count += rvals[i].count;
       reducedValue.total += rvals[i].total;
    }
    return reducedValue;
};
console.log('reduce built');

// finalize 정의
var finalize = function(key, reducedValue) {
    reducedValue.average = reducedValue.total / reducedValue.count;
    return reducedValue;
};
console.log('finalize built');

// command 정의
var command = {
    mapreduce : "user_info",
    map : map.toString(),
    reduce : reduce.toString(),
    query : query,
    out : {replace: "resultjs"},
    finalize : finalize.toString()
};
console.log('command built');

// db가 오픈된 후에 callback으로 M/R job을 돌려야한다.
db.on("open", function(){
    db.db.executeDbCommand(command, function(error, dbres) {
        if (error) throw error;

        console.dir(JSON.stringify(dbres));
        console.dir(dbres.documents[0]);
        console.log('m/r completed');
        console.log('END');
        db.close();
        // db가 close된 후에 callback으로 process가 종료되어야한다.
        db.on("close", function (err) {
            if (err) throw err;
            process.exit(0)
        });
    });
});

