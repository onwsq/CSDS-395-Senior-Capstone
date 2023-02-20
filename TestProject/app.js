var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var bodyParser = require('body-parser');
var app = express();
var AWS = require("aws-sdk");

AWS.config.getCredentials(function(err) {
  if (err) console.log(err.stack);
  // credentials not loaded
  else {
    console.log("Access key:", AWS.config.credentials.accessKeyId);
  }
});

var iconsList = ['fa-solid fa-hippo', 'fa-solid fa-otter', 'fa-solid fa-paw', 'fa-solid fa-cow', 'fa-solid fa-fish', 'fa-solid fa-dog', 'fa-solid fa-worm', 'fa-solid fa-horse', 'fa-solid fa-frog', 'fa-solid fa-cat', 'fa-solid fa-dove'];

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({extended:true}));

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function(req, res, next) {
  res.render('homepage', { title: 'Express' });
});

app.get('/about', function(req, res, next) {
  res.render('about', { title: 'Express' });
});

app.get('/users', async function(req, res, next) {
  var algorithmlist = await getProfiles();
  res.render('users', { algorithmlist: algorithmlist, newProfile: 'no', title: 'Express' });
});

app.get('/results', function(req, res, next) {
  res.render('results', { title: 'Express' });
});

app.get('/newprofile', async function(req, res, next) {
  var algorithmlist = await getProfiles();
  res.render('newprofile', { algorithmlist: algorithmlist,title: 'Express' });
});

app.get('/algorithm', async function(req, res, next) {
  var algorithmlist = await getProfiles();
  console.log(algorithmlist);
  res.render('algorithm', {algorithmlist: algorithmlist, title: 'Express' });
});


app.post('/newprofile', async function(req, res, next) {
  var algorithmlist = await getProfiles();
  var flag = false;
  algorithmlist.forEach(a=>{
    console.log(a[0]);
    console.log(req.body.nickname);
    if(a[0] == req.body.nickname){
      flag = true;
    }
  })
  if(req.body.edit == "true"){
    flag = false;
  }
  if(flag){
    res.render('users', {algorithmlist: algorithmlist, newProfile: 'exists', title: 'Express' });
  }else{
    await sendProfile(req.body.nickname, req.body.username, req.body.password);
    var algorithmlist2 = await getProfiles();
    res.render('users', {algorithmlist: algorithmlist2, newProfile: 'yes', title: 'Express' });
  }
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  console.log(err)
  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

function getProfListBucket(){
  var bucketNameProfList = 'profiles-list'
  var profilesListKeyName = 'profilenames.json'
  var listed = [];

  new Promise((resolve, reject) => {
    new AWS.S3({apiVersion: '2006-03-01'}).getObject({Bucket: bucketNameProfList, Key: profilesListKeyName}, function (err, data) {
        if (err) {

        } else {
            console.log("Successfully dowloaded data from bucket");
            var object = JSON.parse(data.Body.toString());
            var profiles = object.profiles;
            profiles.forEach(p=>{
              listed.push(p);
            })
        }
    });
  });
  return new Promise(resolve=>{
    setTimeout(()=>{
      resolve(listed);
    }, 2000);
  })
}

async function getProfiles(){
  var listtosend = [];

  var results = await getProfListBucket();

  results.forEach(key => {
    var newkey = key + 'userprofile.json'; 
    new Promise((resolve, reject) => {
      new AWS.S3({apiVersion: '2006-03-01'}).getObject({Bucket: 'added-new-person', Key: newkey}, function (err, data) {
          if (err) {
              reject(err);
          } else {
              console.log("Successfully dowloaded data from bucket");
              var object = JSON.parse(data.Body.toString());
              listtosend.push([object.nickname, object.icon, object.password, object.username]);
              resolve(data);
          }
      });
    });
  });
  return new Promise(resolve=>{
    setTimeout(()=>{
      resolve(listtosend);
    }, 2000);
  })
}

function sendProfile(nickname, username, password){
  var bucketNameProfList = 'profiles-list'
  var profilesListKeyName = 'profilenames.json'
  var bucketName = 'added-new-person';
  var keyName = nickname + 'userprofile.json';
  var profilesAll = [];

  new Promise((resolve, reject) => {
    new AWS.S3({apiVersion: '2006-03-01'}).getObject({Bucket: bucketNameProfList, Key: profilesListKeyName}, function (err, data) {
        if (err) {

        } else {
            console.log("Successfully dowloaded data from bucket");
            var object = JSON.parse(data.Body.toString());
            var profiles = object.profiles;
            profiles.forEach(p=>{
              profilesAll.push(p);
            })
        }
    });
  });
  console.log(profilesAll);
  profilesAll.push(nickname);

  var bucketPromise = new AWS.S3({apiVersion: '2006-03-01'}).createBucket({Bucket: bucketName}).promise();
  bucketPromise.then(
    function(data) {
      var objectParams = {
        Bucket: bucketName, 
        Key: keyName, 
        Body: JSON.stringify({
          'nickname': nickname, 
          'username': username,
          'password': password, 
          'icon': iconsList[Math.floor(Math.random()*iconsList.length) | 0]
        })};
      var uploadPromise = new AWS.S3({apiVersion: '2006-03-01'}).putObject(objectParams).promise();
      uploadPromise.then(
        function(data) {
          console.log("Successfully uploaded data to " + bucketName + "/" + keyName);
        });
  }).catch(
    function(err) {
      console.error(err, err.stack);
  });

  var bucketPromise = new AWS.S3({apiVersion: '2006-03-01'}).createBucket({Bucket: bucketNameProfList}).promise();
  bucketPromise.then(
    function(data) {
      var objectParams = {
        Bucket: bucketNameProfList, 
        Key: profilesListKeyName, 
        Body: JSON.stringify({
          'profiles': profilesAll
        })};
      var uploadPromise = new AWS.S3({apiVersion: '2006-03-01'}).putObject(objectParams).promise();
      uploadPromise.then(
        function(data) {
          console.log("Successfully uploaded data to " + bucketName + "/" + keyName);
        });
  }).catch(
    function(err) {
      console.error(err, err.stack);
  });
}


module.exports = app;
