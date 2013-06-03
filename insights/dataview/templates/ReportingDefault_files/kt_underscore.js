// Utility functions which extend Underscore.js
_.mixin({
    // Perform a function on each of an object's values
    mapVals: function(obj, iterator, context) {
        var results = {};
        _.each(obj, function(value, key, list) {
            results[key] = iterator.call(context, obj[key], key, list);
        }, context);
        return results;
    },
    // Pass in a list of keys and a list of values, get an object
    toObject: function(keys, vals) {
        var results = {};
        var zipped = _.zip(keys, vals);
        _(zipped).each(function(entry) {
            results[entry[0]] = entry[1];
        });
        return results;
    }
});
