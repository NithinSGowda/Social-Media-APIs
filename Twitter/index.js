// Open a realtime stream of Tweets, filtered according to rules
// https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/quick-start
const uri = "mongodb://localhost:27017/smmpanel";
const mongoose = require('mongoose');
mongoose.connect(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
    })
    .then(() => {
    console.log('Connected')
}).catch(err => console.log(err))
const tweetModel = new mongoose.Schema({ tweetid: 'string', data: 'string', tag: 'string'},{timestamps: true});
const tweeter = mongoose.model('tweets', tweetModel);

const needle = require('needle');

const token = 'AAAAAAAAAAAAAAAAAAAAALWpLwEAAAAAOQaOYqona1lzhe4pvwxwk3wmFfU%3Dify9vCYjUWGdgzWQ1xhStB6rPg3r3rHTXLmnc8kPQs0ccrRt6c';

const rulesURL = 'https://api.twitter.com/2/tweets/search/stream/rules';
const streamURL = 'https://api.twitter.com/2/tweets/search/stream';

const rules = [{
        'value': 'tesla',
        'tag': 'dog pictures'
    }
];

async function getAllRules() {

    const response = await needle('get', rulesURL, {
        headers: {
            "authorization": `Bearer ${token}`
        }
    })

    if (response.statusCode !== 200) {
        console.log("Error:", response.statusMessage, response.statusCode)
        throw new Error(response.body);
    }

    return (response.body);
}

async function deleteAllRules(rules) {

    if (!Array.isArray(rules.data)) {
        return null;
    }

    const ids = rules.data.map(rule => rule.id);

    const data = {
        "delete": {
            "ids": ids
        }
    }

    const response = await needle('post', rulesURL, data, {
        headers: {
            "content-type": "application/json",
            "authorization": `Bearer ${token}`
        }
    })

    if (response.statusCode !== 200) {
        throw new Error(response.body);
    }

    return (response.body);

}

async function setRules() {

    const data = {
        "add": rules
    }

    const response = await needle('post', rulesURL, data, {
        headers: {
            "content-type": "application/json",
            "authorization": `Bearer ${token}`
        }
    })

    if (response.statusCode !== 201) {
        throw new Error(response.body);
    }

    return (response.body);

}

function streamConnect(retryAttempt) {

    const stream = needle.get(streamURL, {
        headers: {
            "User-Agent": "v2FilterStreamJS",
            "Authorization": `Bearer ${token}`
        },
        timeout: 20000
    });

    stream.on('data', data => {
        try {
            const json = JSON.parse(data);
            // console.log(json);
            obj={}
            obj["tweetid"]=json["data"]["id"]
            obj["data"]=json["data"]["text"]
            obj["tag"]=json["matching_rules"][0]["tag"]
            console.log(obj);
            tweeter.create(obj, function (err, obj2) {
                if (err)
                    console.log(err);
                console.log(obj2)
            });
            // A successful connection resets retry count.
            retryAttempt = 1;
        } catch (e) {
            if (data.detail === "This stream is currently at the maximum allowed connection limit.") {
                console.log(data.detail)
                process.exit(1)
            } else {
                // Keep alive signal received. Do nothing.
            }
        }
    }).on('err', error => {
        if (error.code !== 'ECONNRESET') {
            console.log(error.code);
            process.exit(1);
        } else {
            // This reconnection logic will attempt to reconnect when a disconnection is detected.
            // To avoid rate limits, this logic implements exponential backoff, so the wait time
            // will increase if the client cannot reconnect to the stream. 
            setTimeout(() => {
                console.warn("A connection error occurred. Reconnecting...")
                streamConnect(++retryAttempt);
            }, 2 ** retryAttempt)
        }
    });

    return stream;

}


(async () => {
    let currentRules;

    try {
        // Gets the complete list of rules currently applied to the stream
        currentRules = await getAllRules();

        // Delete all rules. Comment the line below if you want to keep your existing rules.
        await deleteAllRules(currentRules);

        // Add rules to the stream. Comment the line below if you don't want to add new rules.
        await setRules();

    } catch (e) {
        console.error(e);
        process.exit(1);
    }

    // Listen to the stream.
    streamConnect(0);
})();