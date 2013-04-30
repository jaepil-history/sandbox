/**
 * Created with JetBrains WebStorm.
 * User: byouloh
 * Date: 13. 4. 10
 * Time: 오후 4:51
 * To change this template use File | Settings | File Templates.
 */

var mongodb = require('mongodb'),
    server = new mongodb.Server("localhost", 27017, {}),
    sys = require('util'),
    db = new mongodb.Db('test', server, {});

db.open(function (error, client) {
    if (error) throw error;
    var mapFn = function(){
        var n = this.someArray.length
        emit(
            this._id,
            {
                someArrayVals : (n > 0 ? n : 0)
            }
        );
    }
    var reduceFn = function(key, values) {
        var sum = 0;
        var rows = 0;
        values.forEach(function(doc) {
            sum += doc.someArrayVals;
            rows += 1;
        });
        return {someArrayVals: sum, rows : rows  };
    };

    var MR = {
        mapreduce: "user_info",
        out:  { inline : 1 },
        map: mapFn.toString(),
        reduce: reduceFn.toString()
    }

    db.executeDbCommand(MR, function(err, dbres) {
        if (err) {
            console.log('MR error occured');
        }
        else {
            var results = dbres.documents[0].results;
            console.log("executing map reduce, results:");
            console.log(JSON.stringify(results));
            db.close();
            db.on("close", function (err) {
                if (err) throw err;
                process.exit(0)
            });
        }
    });
});