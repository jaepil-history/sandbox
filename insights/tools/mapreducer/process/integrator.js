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

module.exports = new Integrator();