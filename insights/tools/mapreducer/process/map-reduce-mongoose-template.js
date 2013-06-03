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
var db = mongoose.connection;

var StatsReport = require('../models/statsReport')
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
console.log(mr.query);

mr.map = function () {
    var mkey = {gender: this.gender, country: this.country};
    var mval = {count: 1, total: this.purchase};
    emit (mkey, mval);
};

mr.reduce = function (rkey,rvals) {
    var reducedValue = {count: 0, total: 0};
    for (var i = 0; i < rvals.length; i++) {
        reducedValue.count += rvals[i].count;
        reducedValue.total += rvals[i].total;
    }
    return reducedValue;
};

mr.finalize = function(key, reducedValue) {
    reducedValue.average = reducedValue.total / reducedValue.count;
    return reducedValue;
};

mr.out = {merge: "resultjs"};
mr.verbose = true;

exports.doMapReduce = function(option, callback) {

    var result = new StatsReport();
    result.timestamp = Date.now();

    UserInfo.mapReduce(mr, function (err, results, stats) {
        if (err) {
            console.log(err);
        }
        else {
            console.log('m/r completed');
            console.log(stats);

            result.processtime = stats.processtime;
            result.counts = stats.counts;
            result.timing = stats.timing;

            result.save(function (err) {
                if (err) throw err;
                console.log('stats is saved...');
            })
        }
    });

}

