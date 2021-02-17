const Instagram = require('instagram-web-api')
require('dotenv').config()
const app = require('express')();

const { username, password } = process.env
var request = require('request');
var options = {
    'method': 'GET',
    'url': 'https://nithins.me/nbot/instaUpdate.php'
};

const client = new Instagram({ username, password })

app.get('/i', async (req, res) => {
        await client.login()
        const profile = await client.getProfile()
        client.getMediaFeedByHashtag({ hashtag: 'pesuniversity' }).then((data)=>{
            res.send(data)
        })   
})

app.listen(8080, () => console.log(`App is now listening for requests v0.1`));





 
// ;(async () => {
//     await client.login()
//     const profile = await client.getProfile()
//     var n=0;
//     setInterval(()=>{
//         var d = new Date();
//         n+=1;
//         request(options, async function (error, response) {
//             if (error) throw new Error(error);
//             resAns = JSON.parse(response.body)
//             biography = `The time is ${d.getHours()}:${d.getHours()}:${d.getMinutes()} \n Bot Stats : ${resAns["classes"]} classes for ${resAns["users"]} users\n Portfolio Stats : ${resAns["personalVisitors"]} visitors`;

//             await client.updateProfile({
//                 biography: biography, // new bio
//                 website: 'https://nbot.live', // new website
//                 name: profile.fullname, // new name
//                 email: profile.email, // email from profile
//                 username: profile.username, // username from profile
//                 phoneNumber: profile.phone_number, // phone from profile
//                 gender: profile.gender // gender from profile
//             });

//             console.log('Update ' + n);
//         });
//     },10000)

// })()