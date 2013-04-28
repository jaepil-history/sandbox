/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 15
 * Time: 오후 2:00
 * To change this template use File | Settings | File Templates.
 */

//Collection : user_info
//Schema
//{
//    "_id" : ObjectId("51552ed51c0d1810f68446a0"),
//    "purchase" : 0,                    # 구매액
//    "ts" : 1,                          # 타임스템프
//    "uuid" : NumberLong(1)             # 유저 유니크 ID
//    "gender": "none"                   # female/male/none
//    "country": ""                      # 지역명
//    "birthday":""                      # 생년월일
//    "friends_count":0                  # 친구숫자
//}

var mongoose = require('mongoose');

// db 연결
mongoose.connect('mongodb://localhost:27017/test');
var db = mongoose.connection;
console.log('Connected to DB test');

console.log('BEGIN');

// Everything in Mongoose starts with a Schema. Each schema maps to a MongoDB collection and
// defines the shape of the documents within that collection.
var userSchema = new mongoose.Schema({
    purchase : Number,                    // 구매액
    ts : Number,                          // 타임스템프
    uuid : Number,             // 유저 유니크 ID
    gender: String,                   // female/male/none
    country: String,                      // 지역명
    birthday: Date,                      // 생년월일
    friends_count: Number,                // 친구숫자
    age: Number
}, {collection: 'user_info'}); // 마지막은 collection name. 없으면 model_name = collection_name

// mapping UserInfo model to userSchema
var UserInfo = mongoose.model('UserInfo', userSchema);

var mr = {};

mr.query = {"ts": {$gte: 900}};
//query = {"_id.ts":{$gte:12060500,$lte:12060523}};
console.log(mr.query);

mr.map = function () {
    var mkey = {gender: this.gender, country: this.country};
    var mval = {count: 1, total: this.purchase};
    emit (mkey, mval);
};
console.log('map built');

mr.reduce = function (rkey,rvals) {
    var reducedValue = {count: 0, total: 0};
    for (var i = 0; i < rvals.length; i++) {
       reducedValue.count += rvals[i].count;
       reducedValue.total += rvals[i].total;
    }
    return reducedValue;
};
console.log('reduce built');

mr.finalize = function(key, reducedValue) {
    reducedValue.average = reducedValue.total / reducedValue.count;
    return reducedValue;
};
console.log('finalize built');

mr.out = {replace: "resultjs"};
mr.verbose = true;


// db가 오픈된 후에 callback으로 M/R job을 돌려야한다.
db.on("open", function(){
    UserInfo.mapReduce(mr, function (err, results, stats) {
        if (err) {
            console.log(err);
            db.close();
            // db가 close된 후에 callback으로 process를 종료시켜야한다.
            db.on("close", function() {
                process.exit(1);
            });
        }
        else {
            console.log('used mongoose.model');
            console.log('m/r completed');
            console.log(stats);
            console.log('END');
            db.close();
            // db가 close된 후에 callback으로 process를 종료시켜야한다.
            db.on("close", function() {
                process.exit(0);
            });
        }
    });
});


