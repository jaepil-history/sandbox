module.exports = {
    mongodb: {
        server:   'localhost',
        port: 27017,
        database: 'test',
        user: '',
        password: '',
        connectionString: ''      // alternative to setting server, database, user and password separately
    },

    processor: {
        name:                   'origin',
        apiUrl:                 'http://localhost:8888/api', // must be accessible without a proxy
        interval:               10000,     // ten seconds
        timeout:                5000,      // five seconds
        userAgent:              'NodeDataPro/1.0 (https://github.com/appspand/datapro)'
    },

    autoStartDataPro: true,

    server: {
        port:     8888
    },

    email: {
        method:         'SMTP',  // possible methods are SMTP, SES, or Sendmail
        transport:      '',   // see https://github.com/andris9/nodemailer for transport options
        service:        'Gmail', // see https://github.com/andris9/Nodemailer/blob/master/lib/wellknown.js for well-known services
        auth: '',
        user: '',        // The email account username, e.g. 'username@gmail.com'
        pass: '',         // The email account password, e.G. 'password'
        event:'',
        up:        true,
        down:      true,
        paused:    false,
        restarted: false,
        message: '',
        from:    '',         // The message sender, e.g. 'Fred Foo <foo@blurdybloop.com>'
        to:      '',        // The message recipient, e.g. 'bar@blurdybloop.com, baz@blurdybloop.com'
        dashboardUrl: 'http://localhost:8888'
    },
        
    verbose: true // only used in dev
}