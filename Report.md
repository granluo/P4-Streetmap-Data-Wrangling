# OpenStreetMap Data Case Study

### Map Area

San Jose, CA, United States

  - [Map Area In OpenStreetMap](https://www.openstreetmap.org/export#map=10/37.3008/-121.7628)
  - [Documents From Mapzen(OSM file for this project)](https://mapzen.com/data/metro-extracts/metro/san-jose_california/)

This map is of where I live now. I like Bay Area so much and so I moved to Mountain View right after my graduation in Cleveland, OH, but I still support Cavaliers!
I am eager to get familiar to where I newly move in and I am so grad I can take this chance to contribute to the improvements.


### Problems Encountered in the Map

After [downloading the dataset](https://s3.amazonaws.com/metro-extracts.mapzen.com/san-jose_california.osm.bz2), I took a small sample size of the San Jose area and ran it against _audit.py_, I found four problems in the data.

  - Street names: over­abbreviated and misspelled street names and mixed street names with units
    - Blake Ave （Ave to Avenue)
    - Los Gatos Boulvevard (Boulvevard to Boulevard)
    - West Evelyn Avenue Suite #114 (Suite #114 should be removed)
  - City names: misspelled city names, inconsistent case sensitivity and inconsistent format
    - Los Gato (Los Gato to Los Gatos)
    - Santa clara, SUnnyvale (clara to Clara, SUnnyvale to Sunnyvale)
    - San Jos\xe9 (should be San Jose)
  - Phone number: inconsistent formats
    - Various formats:(408) 238-2086,(1)(408) 766-7000,(408)-252-5299,+ 408 980 6400, +1 408 2626949, etc..
    - All these different formats should be unified
  - Postal code: inconsistent formats
    - Various formats: CA 95116,95134-1358,'95014-2143;95014-2144'，u'94087\u200e',
    - The data has various formats of postal codes, which should be unified.

Before updating all the data and fixing problems above, I ran _audit.py_ to read over the entire dataset and find out all different types of expressions and formats. And so I can create different mappings and methods of compilations to cover all different formats.

##### Street Names
To correct street names, I iterated each word in an address and correct it to its corresponding mapping in _audit.py_ using the following function:
```s
def update_street_name(name):
    name = name.title()
    if "," in name:
        name = name.split(',')[0] # remove city and states
    name_array = name.split(' ')
    for i in range(len(name_array)):
        if name_array[i] in street_mapping:
            if name_array[i].lower() not in ['suite','ste','ste.']: #letter after suites represent its corresponding building, not an abbreviation
                name_array[i] = street_mapping[name_array[i]]
            else:
                name_array[i] = street_mapping[name_array[i]]
                break
    return ' '.join(name_array)
```

This updated all street names, such as Great America Pkwy ste 201 to Great America Parkway Suite 201

##### City names

Since San Jose has a certain number of counties, after setting each county name in a common format, like case sensitivity, I only have couple city names out of expectations through the whole dataset and so I will have these names corrected by mapping.

##### Phone number
I set up a format that all phone numbers should follow, which is like "+1 408 200 4868". Since some of the phone numbers had letters representing numbers, I replaced letters back to numbers. After making sure all numbers are digits, I cleaned phone numbers by removing all symbols, including spaces, not digits, and I would have numbers with consecutive 10 digits or 11 digits, which I edited then to the format for phone numbers.
```s
def update_phone_num(num):
    m = phone_type_re.match(num)
    keypad = {'2':'ABCabc','3':'DEFdef','4':'GHIghi','5':'JKLjkl','6':'MNOmno','7':'PQRSpqrs','8':'TUVtuv','9':'WXYZwxyz'}
    if m is None:
        if re.search(r'[a-zA-Z]',num) is not None: #transfer letters to digits
            for key in keypad:
                num = re.sub(r'['+keypad[key]+']',key,num)
        if '-' in  num:   # Remove all possible punctuations
            num = re.sub('-','',num)
        if '.' in num:
            num = re.sub('\.','',num)
        if '(' in num or ')' in num:
            num = re.sub('[()]','',num)
        num = re.sub('\s+','',num)
        if re.search(r'\d{11}',num) is not None:
            num = re.search(r'\d{11}',num).group()
            num = num[:1] + ' ' + num[1:4] + ' ' + num[4:7] + ' ' +num[7:]
        if re.search(r'\d{10}',num) is not None:
            num = re.search(r'\d{10}',num).group()
            num = num[:3] + ' ' + num[3:6] + ' ' +num[6:]
        if re.match(r'\d{3}\s\d{3}\s\d{4}', num):
            num = '+1 ' +num
        if re.match(r'1\s\d{3}\s\d{3}\s\d{4}',num):
            num = '+'+ num
        if re.match(r'\+1\d{10}$',num) is not None:
            num = num[:2] + ' ' + num[2:5] + ' ' + num[5:8] + ' ' +num[8:]
    return num

```

##### Postal code

For the part of postal code, I only kept the postal codes with 5 digits, instead of the one with 9 digits. Since not all postal codes have 9 digits, in order to keep a common format, I removed the last 4 digits if they have 9.

##### For data cannot be updated

After updating all the data, I audited it again and found some data cannot be updated. I found "+1","2924779" in phone number and 'CUPERTINO' in postal code. Data like this might not be able to be updated unless it has more information. However, I will still keep it and move it to the database since at least, we can still dig some information from them, which, though, are not perfect.

### Overview of the data
This section contains basic statistics about the dataset, the SQL queries used to gather them, and some additional ideas about the data in context.

##### File sizes
```
san-jose_california.osm ......... 343 MB
mydb.db ......................... 204 MB
nodes.csv ....................... 133 MB
nodes_tags.csv .................. 2.82 MB
ways.csv ........................ 13.0 MB
ways_tags.csv ................... 20.3 MB
ways_nodes.cv ................... 45.7 MB  
```
##### Number of unique users
```
Count_of_users
1334            
```
##### Number of nodes
```
Number_of_Nodes
1657147
 ```       
##### Number of ways
```
Number_of_Ways
226154          
```
##### Top 10 users of contribution
```
User           Number_of_Contributions
andygol         295728          
nmixter         285524          
mk408           148037          
Bike Mapper     90980           
samely          81414           
RichRico        75663           
dannykath       73014           
karitotp        62436           
MustangBuyer    51667           
Minh Nguyen     43793           
```
##### Number of one-time contributors
```
first_time_contribution_user
289             
```


To improve,

  - Create an additional column for 4 digits of postal codes which have them.

  - Drag and drop images (requires your Dropbox account be linkedEcountered in the Map

You can also:
  - Import and save files from GitHub, Dropbox, Google Drive and One Drive
  - Drag and drop markdown and HTML files into Dillinger
  - Export documents as Markdown, HTML and PDF

Markdown is a lightweight markup language based on the formatting conventions that people naturally use in email.  As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Tech

Dillinger uses a number of open source projects to work properly:

* [AngularJS] - HTML enhanced for web apps!
* [Ace Editor] - awesome web-based text editor
* [markdown-it] - Markdown parser done right. Fast and easy to extend.
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [node.js] - evented I/O for the backend
* [Express] - fast node.js network app framework [@tjholowaychuk]
* [Gulp] - the streaming build system
* [Breakdance](http://breakdance.io) - HTML to Markdown converter
* [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

### Installation

Dillinger requires [Node.js](https://nodejs.org/) v4+ to run.

Install the dependencies and devDependencies and start the server.

```sh
$ cd dillinger
$ npm install -d
$ node app
```

For production environments...

```sh
$ npm install --production
$ npm run predeploy
$ NODE_ENV=production node app
```

### Plugins

Dillinger is currently extended with the following plugins. Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md] [PlDb] |
| Github | [plugins/github/README.md] [PlGh] |
| Google Drive | [plugins/googledrive/README.md] [PlGd] |
| OneDrive | [plugins/onedrive/README.md] [PlOd] |
| Medium | [plugins/medium/README.md] [PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md] [PlGa] |


### Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantanously see your updates!

Open your favorite Terminal and run these commands.

First Tab:
```sh
$ node app
```

Second Tab:
```sh
$ gulp watch
```

(optional) Third:
```sh
$ karma test
```
##### Building for source
For production release:
```sh
$ gulp build --prod
```
Generating pre-built zip archives for distribution:
```sh
$ gulp build dist --prod
```
### Docker
Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 80, so change this within the Dockerfile if necessary. When ready, simply use the Dockerfile to build the image.

```sh
cd dillinger
docker build -t joemccann/dillinger:${package.json.version}
```
This will create the dillinger image and pull in the necessary dependencies. Be sure to swap out `${package.json.version}` with the actual version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on your host. In this example, we simply map port 8000 of the host to port 80 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart="always" <youruser>/dillinger:${package.json.version}
```

Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8000
```

##### Kubernetes + Google Cloud

See [KUBERNETES.md](https://github.com/joemccann/dillinger/blob/master/KUBERNETES.md)


### Todos

 - Write MOAR Tests
 - Add Night Mode

License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
