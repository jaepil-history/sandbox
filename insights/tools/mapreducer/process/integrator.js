<<<<<<< HEAD
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
//var IntervalBuilder = require('../lib/intervalBuilder');

var Integrator = function() {
};

Integrator.prototype.join = function() {
    dbclient.db_appspand.collection('application').find({}, {'cluster':1, 'name':1}, function (err, apps) {
        if (err) throw err;

        var appId;

        for (var i in apps) {
            appId = apps[i]._id.toString();
            joinAllandCPU(appId, function(err) {if(err) throw err; return true});
        }
    });
};

var joinAllandCPU = function(appId, callback) {
    var cpu_collection = appId + '.event.cpu';
    var all_collection = appId + '.event.all';
    var integration_collection = appId + '.integration';

    dbclient.db_insight.collection(all_collection).find({}, function(err, docs) {
        if(err) throw err;
        if(!docs) {
            console.log('No docs to be integrated found');
            dbclient.db_insight.close();
        }
        else {
            var today = new Date();
            console.log(today);
            docs.forEach(function(doc) {
                if(doc.uuid) {
                    dbclient.db_insight.collection(cpu_collection).findOne({'uuid': doc.uuid}, function(err, cpu) {
                        if (err) throw err;
                        //console.log(cpu_collection);
                        //console.log(cpu);
                        doc['b'] = cpu.b;
                        doc['g'] = cpu.g;
                        doc['f'] = cpu.f;
                        doc['lc'] = cpu.lc;
                        doc['age'] = today.getFullYear() - cpu.b.split('/', 1);
                        dbclient.db_processed.collection(integration_collection).insert(doc, function (err, inserted) {
                            if (err) throw err;
                            //console.log(inserted);
                        });
                    });
                }
                else {
                    dbclient.db_processed.collection(integration_collection).insert(doc, function (err, inserted) {
                        if (err) throw err;
                        //console.log(inserted);
                    });
                }
                console.log('inserted');
            });
            //db_insight.close();
            //db_processed.close();
        }
    });
};

=======
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
//var IntervalBuilder = require('../lib/intervalBuilder');

var Integrator = function() {
};

Integrator.prototype.join = function() {
    dbclient.db_appspand.collection('application').find({}, {'cluster':1, 'name':1}, function (err, apps) {
        if (err) throw err;

        var appId;

        for (var i in apps) {
            appId = apps[i]._id.toString();
            joinAllandCPU(appId, function(err, handled) {
                if(err || !handled) {
                    console.log("Error in handling data");
                    throw err;
                }
                //return true;
            });
        }
    });
//
//    var start = +new Date();
//    var counter = 0;
//    for (var i = 1; i < LIMIT; i++) {
//        ++counter;
//        db.users.save({id : i, name : "MongoUser [" + i + "]"}, function(err, saved) {
//            if( err || !saved ) console.log("Error");
//            else console.log("Saved");
//            if (--counter === 0) {
//                var end = +new Date();
//                console.log("all users saved in " + (end-start) + " milliseconds");
//            }
//        });
//    }
};

var joinAllandCPU = function(appId, callback) {
    var cpu_collection = appId + '.event.cpu';
    var all_collection = appId + '.event.all';
    var integration_collection = appId + '.integration';

    var start = new Date();
    var counter = 0;

    dbclient.db_insight.collection(all_collection).find({}, function(err, docs) {
        if(err) throw err;
        if(!docs) {
            console.log('No docs to be integrated found');
            dbclient.db_insight.close();
        }
        else {
            ++counter;
            var today = new Date();
            console.log(docs.length);
            docs.forEach(function(doc) {
                if(doc.uuid) {
                    dbclient.db_insight.collection(cpu_collection).findOne({'uuid': doc.uuid}, function(err, cpu) {
                        if (err) throw err;
                        //console.log(cpu_collection);
                        //console.log(cpu);
                        doc['b'] = cpu.b;
                        doc['g'] = cpu.g;
                        doc['f'] = cpu.f;
                        doc['lc'] = cpu.lc;
                        doc['age'] = today.getFullYear() - cpu.b.split('/', 1);
                        dbclient.db_processed.collection(integration_collection).insert(doc, function (err, inserted) {
                            if (err) throw err;
                            //console.log(inserted);
                            if (--counter === 0) {
                                var end = new Date();
                                console.log("all users saved in " + (end-start) + " milliseconds");
                            }
                        });
                    });
                }
                else {
                    dbclient.db_processed.collection(integration_collection).insert(doc, function (err, inserted) {
                        if (err) throw err;
                        //console.log(inserted);
                        if (--counter === 0) {
                            var end = new Date();
                            console.log("all users saved in " + (end-start) + " milliseconds");
                        }
                    });
                }
                //console.log('inserted');
            });
            //db_insight.close();
            //db_processed.close();
        }
    });
};

>>>>>>> e1fa4f7d9c8eb0592f3156be59486cb533826530
module.exports = new Integrator();