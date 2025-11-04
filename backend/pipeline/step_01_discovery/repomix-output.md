DOCS


## Keyword Ide‌as
The Keyword Ideas endpoint provides search terms that are relevant to the product or service categories of the specified keywords. The algorithm selects the keywords which fall into the same categories as the seed keywords specified in a POST array.
As a result, you will get a list of relevant keyword ideas for up to 200 seed keywords.
Along with each keyword idea, you will get its search volume rate for the last month, search volume trend for the previous 12 months, as well as current cost-per-click and competition values. Moreover, this endpoint supplies minimum, maximum and average values of clicks and CPC for each result.
**Datasource:** DataForSEO Keyword Database segmented by product categories.
**Search algorithm:** relevance-based search for terms that fall into the same category as specified seed keywords.
**Examples:**
Note: no additional sorting parameters applied, `"closely_variants"` set to `false`
Specified seed keywords:
_“keyword research”_, _“content marketing”_
Resulting keyword ideas:
_•”free adword tools”,_
_•”find longtail keywords”,_
_•”how to do keywords research”,_
_•”seo keyword research template”_
> Instead of ‘login’ and ‘password’ use your credentials from https://app.dataforseo.com/api-access
```
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"
curl --location --request POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json" \
--data-raw '[\
{\
"keywords": [\
"phone",\
"watch"\
],\
"location_code": 2840,\
"language_code": "en",\
"include_serp_info": true,\
"limit": 3\
}\
]'
```
```
// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip
require('RestClient.php');
$api_url = 'https://api.dataforseo.com/';
// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
$client = new RestClient($api_url, null, 'login', 'password');
$post_array = array();
// simple way to set a task
$post_array[] = array(
"keywords" => [\
"phone",\
"watch"\
],
"language_name" => "English",
"location_code" => 2840,
"filters" => [\
["keyword_info.search_volume", ">", 10]\
],
"limit" => 3
);
try {
// POST /v3/dataforseo_labs/google/keyword_ideas/live
$result = $client->post('/v3/dataforseo_labs/google/keyword_ideas/live', $post_array);
print_r($result);
// do something with post result
} catch (RestClientException $e) {
echo "n";
print "HTTP code: {$e->getHttpCode()}n";
print "Error code: {$e->getCode()}n";
print "Message: {$e->getMessage()}n";
print $e->getTraceAsString();
echo "n";
}
$client = null;
?>
```
```
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
keywords=[\
"phone",\
"watch"\
],
location_name="United States",
language_name="English",
filters=[\
["keyword_info.search_volume", ">", 10]\
],
limit=3
)
# POST /v3/dataforseo_labs/google/keyword_ideas/live
response = client.post("/v3/dataforseo_labs/google/keyword_ideas/live", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
print(response)
# do something with result
else:
print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
```
```
const post_array = [];
post_array.push({
"keywords": [\
"phone",\
"watch"\
],
"location_code": 2840,
"language_name": "English",
"filters": [\
["keyword_info.search_volume", ">", 10]\
],
"limit": 3
});
const axios = require('axios');
axios({
method: 'post',
url: 'https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live',
auth: {
username: 'login',
password: 'password'
},
data: post_array,
headers: {
'content-type': 'application/json'
}
}).then(function (response) {
var result = response['data']['tasks'];
// Result data
console.log(result);
}).catch(function (error) {
console.log(error);
});
```
```
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
namespace DataForSeoDemos
{
public static partial class Demos
{
public static async Task dataforseo_labs_google_keyword_ideas_live()
{
var httpClient = new HttpClient
{
BaseAddress = new Uri("https://api.dataforseo.com/"),
// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
};
var postData = new List();
postData.Add(new
{
keywords = new[]
{
"phone",
"watch"
},
location_name = "United States",
language_name = "English",
filters = new object[]
{
new object[] { "keyword_info.search_volume", ">", 10 }
},
limit = 3
});
// POST /v3/dataforseo_labs/google/keyword_ideas/live
// the full list of possible parameters is available in documentation
var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/keyword_ideas/live", new StringContent(JsonConvert.SerializeObject(postData)));
var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());
// you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if (result.status_code == 20000)
{
// do something with result
Console.WriteLine(result);
}
else
Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");
}
}
}
```
> The above command returns JSON structured like this:
```
{
"version": "0.1.20240801",
"status_code": 20000,
"status_message": "Ok.",
"time": "0.7097 sec.",
"cost": 0.0103,
"tasks_count": 1,
"tasks_error": 0,
"tasks": [\
{\
"id": "08221822-1535-0400-0000-8fccf5eb0f23",\
"status_code": 20000,\
"status_message": "Ok.",\
"time": "0.6455 sec.",\
"cost": 0.0103,\
"result_count": 1,\
"path": [\
"v3",\
"dataforseo_labs",\
"google",\
"keyword_ideas",\
"live"\
],\
"data": {\
"api": "dataforseo_labs",\
"function": "keyword_ideas",\
"se_type": "google",\
"keywords": [\
"phone",\
"watch"\
],\
"location_code": 2840,\
"language_code": "en",\
"include_serp_info": true,\
"limit": 3\
},\
"result": [\
{\
"se_type": "google",\
"seed_keywords": [\
"phone",\
"watch"\
],\
"location_code": 2840,\
"language_code": "en",\
"total_count": 533763,\
"items_count": 3,\
"offset": 0,\
"offset_token": "eyJDdXJyZW50T2Zmc2V0IjozLCJSZXF1ZXN0RGF0YSI6eyJrZXl3b3JkcyI6WyJwaG9uZSIsIndhdGNoIl0sImxvY2F0aW9uIjoyODQwLCJsYW5ndWFnZSI6ImVuIiwiY2xvc2VseV92YXJpYW50cyI6ZmFsc2UsIm5ld2VzdCI6ZmFsc2UsImV4dGVuZGVkIjpmYWxzZSwibG9hZF9zZXJwX2luZm8iOnRydWUsImF1dG9jb3JyZWN0Ijp0cnVlLCJJc09sZCI6ZmFsc2UsInNlYXJjaF9hZnRlcl90b2tlbiI6bnVsbCwiaWdub3JlX3N5bm9ueW1zIjpmYWxzZSwic2VhcmNoX2VuZ2luZSI6Imdvb2dsZSIsInVzZV9uZXdfY2F0ZWdvcmllcyI6dHJ1ZSwib3JkZXJfYnkiOnsib3JkZXJfZmllbGQiOiJfc2NvcmUiLCJvcmRlcl90eXBlIjoiRGVzYyIsIm5leHQiOm51bGx9LCJsaW1pdCI6Mywib2Zmc2V0IjowLCJhaWQiOjE1MzV9LCJSYXdRdWVyeSI6bnVsbCwiSWQiOiJiNWEyZGNlOS00Mzk3LTQ3NTgtYWEyOC02NWFiMzY3ZDM5NDgiLCJTZWFyY2hBZnRlckRhdGEiOlszMDQuMTc2NTcsImUwNGZkMDE1LTllY2YtMzcwYi0xZGJmLWY0NGExODVjOWU5ZiJdfQ==",\
"items": [\
{\
"se_type": "google",\
"keyword": "phone",\
"location_code": 2840,\
"language_code": "en",\
"keyword_info": {\
"se_type": "google",\
"last_updated_time": "2024-08-11 13:24:34 +00:00",\
"competition": 1,\
"competition_level": "HIGH",\
"cpc": 5.98,\
"search_volume": 368000,\
"low_top_of_page_bid": 3.08,\
"high_top_of_page_bid": 10.5,\
"categories": [\
10007,\
10878,\
12133,\
13381\
],\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 450000\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 368000\
}\
],\
"search_volume_trend": {\
"monthly": 22,\
"quarterly": 22,\
"yearly": 0\
}\
},\
"clickstream_keyword_info": null,\
"keyword_properties": {\
"se_type": "google",\
"core_keyword": null,\
"synonym_clustering_algorithm": "text_processing",\
"keyword_difficulty": 83,\
"detected_language": "en",\
"is_another_language": false\
},\
"serp_info": {\
"se_type": "google",\
"check_url": "https://www.google.com/search?q=phone&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",\
"serp_item_types": [\
"popular_products",\
"images",\
"organic",\
"product_considerations",\
"refine_products",\
"top_stories",\
"related_searches"\
],\
"se_results_count": 19880000000,\
"last_updated_time": "2024-07-14 21:43:34 +00:00",\
"previous_updated_time": "2024-05-18 19:29:28 +00:00"\
},\
"avg_backlinks_info": {\
"se_type": "google",\
"backlinks": 6835.7,\
"dofollow": 3775.6,\
"referring_pages": 5352.2,\
"referring_domains": 1100.3,\
"referring_main_domains": 955.1,\
"rank": 369.3,\
"main_domain_rank": 681.2,\
"last_updated_time": "2024-07-14 21:43:39 +00:00"\
},\
"search_intent_info": {\
"se_type": "google",\
"main_intent": "navigational",\
"foreign_intent": [\
"commercial"\
],\
"last_updated_time": "2023-03-02 03:55:21 +00:00"\
},\
"keyword_info_normalized_with_bing": {\
"last_updated_time": "2024-08-17 01:41:37 +00:00",\
"search_volume": 308309,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 377009\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 308309\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 308309\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 308309\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 308309\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 308309\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 308309\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 308309\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 308309\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 308309\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 308309\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 308309\
},\
{\
"year": 2023,\
"month": 7,\
"search_volume": 300631\
}\
]\
},\
"keyword_info_normalized_with_clickstream": {\
"last_updated_time": "2024-08-17 01:41:37 +00:00",\
"search_volume": 324416,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 396705\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 7,\
"search_volume": 324365\
}\
]\
}\
},\
{\
"se_type": "google",\
"keyword": "cell phone signal booster",\
"location_code": 2840,\
"language_code": "en",\
"keyword_info": {\
"se_type": "google",\
"last_updated_time": "2024-08-11 18:11:54 +00:00",\
"competition": 1,\
"competition_level": "HIGH",\
"cpc": 1.05,\
"search_volume": 22200,\
"low_top_of_page_bid": 0.31,\
"high_top_of_page_bid": 1.15,\
"categories": [\
10007,\
10878,\
12133,\
13381\
],\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 33100\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 18100\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 18100\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 18100\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 18100\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 27100\
}\
],\
"search_volume_trend": {\
"monthly": 22,\
"quarterly": 22,\
"yearly": 0\
}\
},\
"clickstream_keyword_info": null,\
"keyword_properties": {\
"se_type": "google",\
"core_keyword": "cell phone signal booster for phone",\
"synonym_clustering_algorithm": "text_processing",\
"keyword_difficulty": 23,\
"detected_language": "en",\
"is_another_language": false\
},\
"serp_info": {\
"se_type": "google",\
"check_url": "https://www.google.com/search?q=cell%20phone%20signal%20booster&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",\
"serp_item_types": [\
"popular_products",\
"people_also_ask",\
"organic",\
"images",\
"related_searches"\
],\
"se_results_count": 13500000,\
"last_updated_time": "2024-08-04 11:06:04 +00:00",\
"previous_updated_time": "2024-06-22 20:35:21 +00:00"\
},\
"avg_backlinks_info": {\
"se_type": "google",\
"backlinks": 111.6,\
"dofollow": 34.7,\
"referring_pages": 104.5,\
"referring_domains": 29,\
"referring_main_domains": 26.3,\
"rank": 103.5,\
"main_domain_rank": 530.7,\
"last_updated_time": "2024-08-04 11:06:06 +00:00"\
},\
"search_intent_info": {\
"se_type": "google",\
"main_intent": "transactional",\
"foreign_intent": null,\
"last_updated_time": "2023-03-03 12:40:39 +00:00"\
},\
"keyword_info_normalized_with_bing": {\
"last_updated_time": "2024-08-16 10:43:48 +00:00",\
"search_volume": 12895,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 19226\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 15741\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 12895\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 10513\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 10513\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 10513\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 10513\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 12895\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 12895\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 15741\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 15741\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 15741\
},\
{\
"year": 2023,\
"month": 7,\
"search_volume": 19139\
}\
]\
},\
"keyword_info_normalized_with_clickstream": {\
"last_updated_time": "2024-08-16 10:43:48 +00:00",\
"search_volume": 15498,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 23107\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 18918\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 15498\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 12635\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 12635\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 12635\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 12635\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 15498\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 15498\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 18918\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 18918\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 18918\
},\
{\
"year": 2023,\
"month": 7,\
"search_volume": 22930\
}\
]\
}\
},\
{\
"se_type": "google",\
"keyword": "phone charm",\
"location_code": 2840,\
"language_code": "en",\
"keyword_info": {\
"se_type": "google",\
"last_updated_time": "2024-08-12 16:45:18 +00:00",\
"competition": 1,\
"competition_level": "HIGH",\
"cpc": 0.66,\
"search_volume": 27100,\
"low_top_of_page_bid": 0.26,\
"high_top_of_page_bid": 1.93,\
"categories": [\
10007,\
10878,\
12133,\
13381\
],\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 33100\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 27100\
}\
],\
"search_volume_trend": {\
"monthly": 22,\
"quarterly": 22,\
"yearly": 0\
}\
},\
"clickstream_keyword_info": null,\
"keyword_properties": {\
"se_type": "google",\
"core_keyword": "charms for phones",\
"synonym_clustering_algorithm": "text_processing",\
"keyword_difficulty": 0,\
"detected_language": "en",\
"is_another_language": false\
},\
"serp_info": {\
"se_type": "google",\
"check_url": "https://www.google.com/search?q=phone%20charm&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",\
"serp_item_types": [\
"popular_products",\
"organic",\
"people_also_ask",\
"images",\
"explore_brands",\
"related_searches"\
],\
"se_results_count": 284000000,\
"last_updated_time": "2024-08-04 10:21:18 +00:00",\
"previous_updated_time": "2024-06-22 19:50:30 +00:00"\
},\
"avg_backlinks_info": {\
"se_type": "google",\
"backlinks": 15.9,\
"dofollow": 9,\
"referring_pages": 10.5,\
"referring_domains": 3,\
"referring_main_domains": 2.6,\
"rank": 44.1,\
"main_domain_rank": 491.8,\
"last_updated_time": "2024-08-04 10:21:19 +00:00"\
},\
"search_intent_info": {\
"se_type": "google",\
"main_intent": "transactional",\
"foreign_intent": null,\
"last_updated_time": "2023-03-02 03:55:42 +00:00"\
},\
"keyword_info_normalized_with_bing": {\
"last_updated_time": "2024-08-17 03:47:30 +00:00",\
"search_volume": 14892,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 18190\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 14892\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 14892\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 12200\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 14892\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 12200\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 14892\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 14892\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 14892\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 12200\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 12200\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 14892\
},\
{\
"year": 2023,\
"month": 7,\
"search_volume": 15028\
}\
]\
},\
"keyword_info_normalized_with_clickstream": {\
"last_updated_time": "2024-08-17 03:47:30 +00:00",\
"search_volume": 13826,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 16887\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 13826\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 13826\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 11326\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 13826\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 11326\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 13826\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 13826\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 13826\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 11326\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 11326\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 13826\
},\
{\
"year": 2023,\
"month": 7,\
"search_volume": 13822\
}\
]\
}\
}\
]\
}\
]\
}\
]
}
```
**`POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live`**
Your account will be charged for each request.
The cost can be calculated on the [Pricing](https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api "Pricing") page.
All POST data should be sent in the [JSON](https://en.wikipedia.org/wiki/JSON) format (UTF-8 encoding). The task setting is done using the POST method. When setting a task, you should send all task parameters in the task array of the generic POST array. You can send up to 2000 API calls per minute. The maximum number of requests that can be sent simultaneously is limited to 30.
You can specify the number of results you want to retrieve and sort them.
Below you will find a detailed description of the fields you can use for setting a task.
**Description of the fields for setting a task:**
| Field name | Type | Description |
| --- | --- | --- |
| `keywords` | array | _keywords_
**required field**
UTF-8 encoding
The maximum number of keywords you can specify: 200.
The keywords will be converted to lowercase format
learn more about rules and limitations of `keyword` and `keywords` fields in DataForSEO APIs in this [Help Center article](https://dataforseo.com/help-center/rules-and-limitations-of-keyword-and-keywords-fields-in-dataforseo-apis) | |
| `location_name` | string | _full name of the location_
**required field if you don’t specify** `location_code`
**Note:** it is required to specify either `location_name` or `location_code`
you can receive the list of available locations with their `location_name` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`United Kingdom` | |
| `location_code` | integer | _unique location identifier_
**required field if you don’t specify** `location_name`
**Note:** it is required to specify either `location_name` or `location_code`
you can receive the list of available locations with their `location_code` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`2840` | |
| `language_name` | string | _full name of the language_
optional field
if you use this field, you don’t need to specify `language_code`
you can receive the list of available languages with their `language_name` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`English`
**Note:** if omitted, results default to the language with the most keyword records in the specified location;
refer to the `available_languages.keywords` field of the [Locations and Languages endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages) to determine the default language | |
| `language_code` | string | _language code_
optional field
if you use this field, you don’t need to specify `language_name`
you can receive the list of available languages with their `language_code` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`en`
**Note:** if omitted, results default to the language with the most keyword records in the specified location;
refer to the `available_languages.keywords` field of the [Locations and Languages endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages) to determine the default language | |
| `closely_variants` | boolean | _search mode_
optional field
if set to `true` the results will be based on the phrase-match search algorithm
if set to `false` the results will be based on the broad-match search algorithm
default value: `false` | |
| `ignore_synonyms` | boolean | _ignore highly similar keywords_
optional field
if set to `true` only core keywords will be returned, all highly similar keywords will be excluded;
default value: `false` | |
| `include_serp_info` | boolean | _include data from SERP for each keyword_
optional field
if set to `true`, we will return a `serp_info` array containing SERP data (number of search results, relevant URL, and SERP features) for every keyword in the response
default value: `false` | |
| `include_clickstream_data` | boolean | _include or exclude data from clickstream-based metrics in the result_
optional field
if the parameter is set to `true`, you will receive `clickstream_keyword_info`, `keyword_info_normalized_with_clickstream`, and `keyword_info_normalized_with_bing` fields in the response
default value: `false`
with this parameter enabled, you will be charged double the price for the request
learn more about how clickstream-based metrics are calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `limit` | integer | _the maximum number of keywords in the results array_
optional field
default value: `700`
maximum value: `1000` | |
| `offset` | integer | _offset in the results array of returned keywords_
optional field
default value: `0`
if you specify the `10` value, the first ten keywords in the results array will be omitted and the data will be provided for the successive keywords | |
| `offset_token` | string | _offset token for subsequent requests_
optional field
provided in the identical filed of the response to each request;
use this parameter to avoid timeouts while trying to obtain over 10,000 results in a single request;
by specifying the unique `offset_token` value from the response array, you will get the subsequent results of the initial task;
`offset_token` values are unique for each subsequent task
**Note:** if the `offset_token` is specified in the request, all other parameters except `limit` will not be taken into account when processing a task. | |
| `filters` | array | _array of results filtering parameters_
optional field
**you can add several filters at once (8 filters maximum)**
you should set a logical operator `and`, `or` between the conditions
the following operators are supported:
`regex`, `not_regex`, `<`, `<=`, `>`, `>=`, `=`, `<>`, `in`, `not_in`, `match`, `not_match`, `ilike`, `not_ilike`, `like`, `not_like`
you can use the `%` operator with `like` and `not_like`,as well as `ilike`, `not_ilike` to match any string of zero or more characters
**note that you can not filter the results by `relevance`**
example:
`["keyword_info.search_volume",">",0]`
`[["keyword_info.search_volume","in",[0,1000]],
"and",
["keyword_info.competition_level","=","LOW"]]`
`[["keyword_info.search_volume",">",100],
"and",
[["keyword_info.cpc","<",0.5],
"or",
["keyword_info.high_top_of_page_bid","<=",0.5]]]`
for more information about filters, please refer to [Dataforseo Labs – Filters](https://docs.dataforseo.com/v3/dataforseo_labs/filters) or this [help center guide](https://dataforseo.com/help-center/how-to-use-filters-in-dataforseo-labs-api) | |
| `order_by` | array | _results sorting rules_
optional field
you can use the same values as in the `filters` array to sort the results
possible sorting types:
`asc` – results will be sorted in the ascending order
`desc` – results will be sorted in the descending order
you should use a comma to set up a sorting parameter
default rule:
`["relevance,desc"]`
relevance is used as the default sorting rule to provide you with the closest keyword ideas. We recommend using this sorting rule to get highly-relevant search terms. **Note** that `relevance` is only our internal system identifier, so **it can not be used as a filter**, and you will not find this field in the `result` array. The relevance score is based on a similar principle as used in [the Keywords For Keywords](https://docs.dataforseo.com/v3/keywords_data/google/keywords_for_keywords/live/?php) endpoint.
**note that you can set no more than three sorting rules in a single request**
you should use a comma to separate several sorting rules
example:
`["relevance,desc","keyword_info.search_volume,desc"]` | |
| `tag` | string | _user-defined task identifier_
optional field
_the character limit is 255_
you can use this parameter to identify the task and match it with the result
you will find the specified `tag` value in the `data` object of the response | |
‌
As a response of the API server, you will receive [JSON](https://en.wikipedia.org/wiki/JSON)-encoded data containing a `tasks` array with the information specific to the set tasks.
**Description of the fields in the results array:**
| Field name | Type | Description |
| --- | --- | --- |
| `version` | string | _the current version of the API_ | |
| `status_code` | integer | _general status code_
you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors)
**Note:** we strongly recommend designing a necessary system for handling related exceptional or error conditions | |
| `status_message` | string | _general informational message_
you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) | |
| `time` | string | _execution time, seconds_ | |
| `cost` | float | _total tasks cost, USD_ | |
| `tasks_count` | integer | _the number of tasks in the **`tasks`** array_ | |
| `tasks_error` | integer | _the number of tasks in the **`tasks`** array returned with an error_ | |
| **`tasks`** | array | _array of tasks_ | |
| `id` | string | _task identifier_
**unique task identifier in our system in the [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format** | |
| `status_code` | integer | _status code of the task_
generated by DataForSEO; can be within the following range: 10000-60000
you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) | |
| `status_message` | string | _informational message of the task_
you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix-errors/) | |
| `time` | string | _execution time, seconds_ | |
| `cost` | float | _cost of the task, USD_ | |
| `result_count` | integer | _number of elements in the `result` array_ | |
| `path` | array | _URL path_ | |
| `data` | object | _contains the same parameters that you specified in the POST request_ | |
| **`result`** | array | _array of results_ | |
| `se_type` | string | _search engine type_ | |
| `seed_keywords` | array | _keywords in a POST array_
**keywords are returned with decoded %## (plus character ‘+’ will be decoded to a space character)** | |
| `location_code` | integer | _location code in a POST array_ | |
| `language_code` | string | _language code in a POST array_ | |
| `total_count` | integer | _total number of results relevant to your request in our database_ | |
| `items_count` | integer | _number of results returned in the `items` array_ | |
| `offset` | integer | _current offset value_ | |
| `offset_token` | string | _offset token for subsequent requests_
you can use the string provided in this field to get the subsequent results of the initial task;
**note:** `offset_token` values are unique for each subsequent task | |
| `items` | array | _contains keyword ideas and related data_ | |
| `se_type` | string | _search engine type_ | |
| `keyword` | string | _returned keyword idea_ | |
| `location_code` | integer | _location code in a POST array_ | |
| `language_code` | string | _language code in a POST array_ | |
| `keyword_info` | object | _keyword data for the returned keyword idea_ | |
| `se_type` | string | _search engine type_ | |
| `last_updated_time` | string | _date and time when keyword data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `competition` | float | _competition_
represents the relative amount of competition associated with the given keyword;
the value is based on Google Ads data and can be between 0 and 1 (inclusive) | |
| `competition_level` | string | _competition level_
represents the relative level of competition associated with the given keyword in paid SERP only;
possible values: `LOW`, `MEDIUM`, `HIGH`
if competition level is unknown, the value is `null`;
learn more about the metric in [this help center article](https://dataforseo.com/help-center/what-is-competition) | |
| `cpc` | float | _cost-per-click_
represents the average cost per click (USD) historically paid for the keyword | |
| `search_volume` | integer | _average monthly search volume rate_
represents the (approximate) number of searches for the given keyword idea on google.com | |
| `low_top_of_page_bid` | float | _minimum bid for the ad to be displayed at the top of the first page_
indicates the value greater than about 20% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)
the value may differ depending on the location specified in a POST request | |
| `high_top_of_page_bid` | float | _maximum bid for the ad to be displayed at the top of the first page_
indicates the value greater than about 80% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)
the value may differ depending on the location specified in a POST request | |
| `categories` | array | _product and service categories_
you can download the [full list of possible categories](https://cdn.dataforseo.com/v3/categories/categories_dataforseo_labs_2023_10_25.csv) | |
| `monthly_searches` | array | _monthly searches_
represents the (approximate) number of searches on this keyword idea (as available for the past twelve months), targeted to the specified geographic locations | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _monthly average search volume rate_ | |
| `search_volume_trend` | object | _search volume trend changes_
represents search volume change in percent compared to the previous period | |
| `monthly` | integer | _search volume change in percent compared to the previous month_ | |
| `quarterly` | integer | _search volume change in percent compared to the previous quarter_ | |
| `yearly` | integer | _search volume change in percent compared to the previous year_ | |
| `clickstream_keyword_info` | object | _clickstream data for the returned keyword_
to retrieve results for this field, the parameter `include_clickstream_data` must be set to `true` | |
| `search_volume` | integer | _monthly average clickstream search volume rate_ | |
| `last_updated_time` | string | _date and time when the clickstream dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” | |
| `gender_distribution` | object | _distribution of estimated clickstream-based metrics by gender_
learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `female` | integer | _number of female users in the relevant clickstream dataset_ | |
| `male` | integer | _number of male users in the relevant clickstream dataset_ | |
| `age_distribution` | object | _distribution of clickstream-based metrics by age_
learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `18-24` | integer | _number of users in the relevant clickstream dataset that fall within the 18-24 age range_ | |
| `25-34` | integer | _number of users in the relevant clickstream dataset that fall within the 25-34 age range_ | |
| `35-44` | integer | _number of users in the relevant clickstream dataset that fall within the 35-44 age range_ | |
| `45-54` | integer | _number of users in the relevant clickstream dataset that fall within the 45-54 age range_ | |
| `55-64` | integer | _number of users in the relevant clickstream dataset that fall within the 55-64 age range_ | |
| `monthly_searches` | array | _monthly clickstream search volume rates_
array of objects with clickstream search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _clickstream-based search volume rate in a certain month of a year_ | |
| `keyword_properties` | object | _additional information about the keyword_ | |
| `se_type` | string | _search engine type_ | |
| `core_keyword` | string | _main keyword in a group_
contains the main keyword in a group determined by the synonym clustering algorithm
if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` | |
| `synonym_clustering_algorithm` | string | _the algorithm used to identify synonyms_
possible values:
`keyword_metrics` – indicates the algorithm based on `keyword_info` parameters
`text_processing` – indicates the text-based algorithm
if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` | |
| `keyword_difficulty` | integer | _difficulty of ranking in the first top-10 organic results for a keyword_
indicates the chance of getting in top-10 organic results for a keyword on a logarithmic scale from 0 to 100;
calculated by analysing, among other parameters, link profiles of the first 10 pages in SERP;
learn more about the metric in [this help center guide](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated) | |
| `detected_language` | string | _detected language of the keyword_
indicates the language of the keyword as identified by our system | |
| `is_another_language` | boolean | _detected language of the keyword is different from the set language_
if `true`, the language set in the request does not match the language determined by our system for a given keyword | |
| `serp_info` | object | _SERP data_
the value will be `null` if you didn’t set the field `include_serp_info` to `true` in the POST array or if there is no SERP data for this keyword in our database | |
| `se_type` | string | _search engine type_ | |
| `check_url` | string | _direct URL to search engine results_
you can use it to make sure that we provided accurate results | |
| 

| `se_results_count` | string | _number of search results for the returned keyword_ | |
| `last_updated_time` | string | _date and time when SERP data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `previous_updated_time` | string | _previous to the most recent date and time when SERP data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-10-15 12:57:46 +00:00` | |
| `avg_backlinks_info` | object | _backlink data for the returned keyword_
this object provides the average number of backlinks, referring pages and domains, as well as the average rank values among the top-10 webpages ranking organically for the keyword | |
| `se_type` | string | _search engine type_ | |
| `backlinks` | float | _average number of backlinks_ | |
| `dofollow` | float | _average number of dofollow links_ | |
| `referring_pages` | float | _average number of referring pages_ | |
| `referring_domains` | float | _average number of referring domains_ | |
| `referring_main_domains` | float | _average number of referring main domains_ | |
| `rank` | float | _average rank_
learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) | |
| `main_domain_rank` | float | _average main domain rank_
learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) | |
| `last_updated_time` | string | _date and time when backlink data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `search_intent_info` | object | _search intent info for the returned keyword_
learn about search intent in this [help center article](https://dataforseo.com/help-center/search-intent-and-its-types) | |
| `se_type` | string | _search engine type_
possible values: `google` | |
| `main_intent` | string | _main search intent_
possible values: `informational`, `navigational`, `commercial`, `transactional` | |
| `foreign_intent` | array | _supplementary search intents_
possible values: `informational`, `navigational`, `commercial`, `transactional` | |
| `last_updated_time` | string | _date and time when search intent data was last updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| **`keyword_info_normalized_with_bing`** | object | _contains keyword search volume normalized with Bing search volume_ | |
| `last_updated_time` | string | _date and time when the dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `search_volume` | integer | _current search volume rate of a keyword_ | |
| `is_normalized` | boolean | _keyword info is normalized_
if `true`, values are normalized with Bing data | |
| `monthly_searches` | integer | _monthly search volume rates_
array of objects with search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _search volume rate in a certain month of a year_ | |
| **`keyword_info_normalized_with_clickstream`** | object | _contains keyword search volume normalized with clickstream data_ | |
| `last_updated_time` | string | _date and time when the dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `search_volume` | integer | _current search volume rate of a keyword_ | |
| `is_normalized` | boolean | _keyword info is normalized_
if `true`, values are normalized with clickstream data | |
| `monthly_searches` | integer | _monthly search volume rates_
array of objects with search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _search volume rate in a certain month of a year_ | |
‌‌
[cURL](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/?bash#) [php](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/?bash#) [NodeJs](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/?bash#) [Python](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/?bash#) [cSharp](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live/?bash#)
## Keyword Suggestions
‌‌
The Keyword Suggestions endpoint provides search queries that include the specified seed keyword.
The algorithm is based on the full-text search for the specified keyword and therefore returns only those search terms that contain the keyword you set in the POST array with additional words before, after, or within the specified key phrase. Returned keyword suggestions can contain the words from the specified key phrase in a sequence different from the one you specify.
As a result, you will get a list of long-tail keywords with each keyword in the list matching the specified search term.
Along with each suggested keyword, you will get its search volume rate for the last month, search volume trend for the previous 12 months, as well as current cost-per-click and competition values.
**Datasource:** DataForSEO Keyword Database
**Search algorithm:** full-text search for terms that match the specified seed keyword with additional words included before, after, or within the seed key phrase.
**Examples**
Specified seed keyword:
_“keyword research”_
Resulting suggestions:
_•”google research keyword”,_
_•”how to do keyword research”,_
_•”keyword competitor research”,_
_•”how to do keyword research for content marketing”_
> Instead of ‘login’ and ‘password’ use your credentials from https://app.dataforseo.com/api-access
```
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"
curl --location --request POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json" \
--data-raw '[\
{\
"keyword": "phone",\
"location_code": 2840,\
"language_code": "en",\
"include_serp_info": true,\
"include_seed_keyword": true,\
"limit": 1\
}\
]'
```
```
// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip
require('RestClient.php');
$api_url = 'https://api.dataforseo.com/';
// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
$client = new RestClient($api_url, null, 'login', 'password');
$post_array = array();
// simple way to set a task
$post_array[] = array(
"keyword" => "phone",
"language_name" => "English",
"location_code" => 2840,
"include_serp_info"=> true,
"include_seed_keyword"=> true,
"limit" => 1
);
try {
// POST /v3/dataforseo_labs/google/keyword_suggestions/live
$result = $client->post('/v3/dataforseo_labs/google/keyword_suggestions/live', $post_array);
print_r($result);
// do something with post result
} catch (RestClientException $e) {
echo "n";
print "HTTP code: {$e->getHttpCode()}n";
print "Error code: {$e->getCode()}n";
print "Message: {$e->getMessage()}n";
print $e->getTraceAsString();
echo "n";
}
$client = null;
?>
```
```
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
keyword="phone",
location_name="United States",
language_name="English",
include_serp_info=True,
include_seed_keyword=True,
limit=1
)
# POST /v3/dataforseo_labs/google/keyword_suggestions/live
response = client.post("/v3/dataforseo_labs/google/keyword_suggestions/live", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
print(response)
# do something with result
else:
print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
```
```
const post_array = [];
post_array.push({
"keyword": "phone",
"location_code": 2840,
"language_name": "English",
"include_serp_info": true,
"include_seed_keyword": true,
"limit": 1
});
const axios = require('axios');
axios({
method: 'post',
url: 'https://api.dataforseo.com/v3/dataforseo_labs/keyword_suggestions/live',
auth: {
username: 'login',
password: 'password'
},
data: post_array,
headers: {
'content-type': 'application/json'
}
}).then(function (response) {
var result = response['data']['tasks'];
// Result data
console.log(result);
}).catch(function (error) {
console.log(error);
});
```
```
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
namespace DataForSeoDemos
{
public static partial class Demos
{
public static async Task dataforseo_labs_google_keyword_suggestions_live()
{
var httpClient = new HttpClient
{
BaseAddress = new Uri("https://api.dataforseo.com/"),
// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
};
var postData = new List();
postData.Add(new
{
keyword = "phone",
location_name = "United States",
language_name = "English",
include_serp_info = true,
include_seed_keyword = true,
limit = 1
});
// POST /v3/dataforseo_labs/google/keyword_suggestions/live
// the full list of possible parameters is available in documentation
var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/keyword_suggestions/live", new StringContent(JsonConvert.SerializeObject(postData)));
var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());
// you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if (result.status_code == 20000)
{
// do something with result
Console.WriteLine(result);
}
else
Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");
}
}
}
```
> The above command returns JSON structured like this:
```
{
"version": "0.1.20240801",
"status_code": 20000,
"status_message": "Ok.",
"time": "0.2704 sec.",
"cost": 0.0101,
"tasks_count": 1,
"tasks_error": 0,
"tasks": [\
{\
"id": "08221704-1535-0399-0000-0acd15b387ff",\
"status_code": 20000,\
"status_message": "Ok.",\
"time": "0.2019 sec.",\
"cost": 0.0101,\
"result_count": 1,\
"path": [\
"v3",\
"dataforseo_labs",\
"google",\
"keyword_suggestions",\
"live"\
],\
"data": {\
"api": "dataforseo_labs",\
"function": "keyword_suggestions",\
"se_type": "google",\
"keyword": "phone",\
"location_code": 2840,\
"language_code": "en",\
"include_serp_info": true,\
"include_seed_keyword": true,\
"limit": 1\
},\
"result": [\
{\
"se_type": "google",\
"seed_keyword": "phone",\
"seed_keyword_data": {\
"se_type": "google",\
"keyword": "phone",\
"location_code": 2840,\
"language_code": "en",\
"keyword_info": {\
"se_type": "google",\
"last_updated_time": "2024-08-11 13:24:34 +00:00",\
"competition": 1,\
"competition_level": "HIGH",\
"cpc": 5.98,\
"search_volume": 368000,\
"low_top_of_page_bid": 3.08,\
"high_top_of_page_bid": 10.5,\
"categories": [\
10007,\
10878,\
12133,\
13381\
],\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 450000\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 368000\
}\
],\
"search_volume_trend": {\
"monthly": 22,\
"quarterly": 22,\
"yearly": 0\
}\
}\
},\
"clickstream_keyword_info": null,\
"serp_info": {\
"se_type": "google",\
"check_url": "https://www.google.com/search?q=phone&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",\
"serp_item_types": [\
"popular_products",\
"images",\
"organic",\
"product_considerations",\
"refine_products",\
"top_stories",\
"related_searches"\
],\
"se_results_count": 19880000000,\
"last_updated_time": "2024-07-15 00:43:34 +00:00",\
"previous_updated_time": "2024-05-18 22:29:28 +00:00"\
},\
"keyword_properties": {\
"se_type": "google",\
"core_keyword": null,\
"synonym_clustering_algorithm": "text_processing",\
"keyword_difficulty": 83,\
"detected_language": "en",\
"is_another_language": false\
},\
"search_intent_info": {\
"se_type": "google",\
"main_intent": "navigational",\
"foreign_intent": [\
"commercial"\
],\
"last_updated_time": "2023-03-02 03:54:21 +00:00"\
},\
"avg_backlinks_info": {\
"se_type": "google",\
"backlinks": 6835.7,\
"dofollow": 3775.6,\
"referring_pages": 5352.2,\
"referring_domains": 1100.3,\
"referring_main_domains": 955.1,\
"rank": 369.3,\
"main_domain_rank": 681.2,\
"last_updated_time": "2024-07-14 21:43:39 +00:00"\
},\
"keyword_info_normalized_with_bing": {\
"last_updated_time": "2024-08-17 01:41:37 +00:00",\
"search_volume": 324416,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 396705\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 324416\
}\
]\
},\
"keyword_info_normalized_with_clickstream": {\
"last_updated_time": "2024-08-11 13:24:34 +00:00",\
"search_volume": 368000,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 450000\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 368000\
}\
]\
}\
},\
{\
"location_code": 2840,\
"language_code": "en",\
"total_count": 3488300,\
"items_count": 1,\
"offset": 0,\
"offset_token": "eyJDdXJyZW50T2Zmc2V0IjoxLCJSZXF1ZXN0RGF0YSI6eyJrZXl3b3JkIjoicGhvbmUiLCJpbmNsdWRlX3NlZWRfa2V5d29yZCI6dHJ1ZSwiZnVsbF9tYXRjaCI6ZmFsc2UsImxvYWRfc2VycF9pbmZvIjp0cnVlLCJzZWFyY2hfYWZ0ZXJfdG9rZW4iOm51bGwsImlnbm9yZV9zeW5vbnltcyI6ZmFsc2UsImxhbmd1YWdlIjoiZW4iLCJzZWFyY2hfZW5naW5lIjoiZ29vZ2xlIiwibG9jYXRpb24iOjI4NDAsInVzZV9uZXdfY2F0ZWdvcmllcyI6dHJ1ZSwib3JkZXJfYnkiOnsib3JkZXJfZmllbGQiOiJrZXl3b3JkX2luZm8uc2VhcmNoX3ZvbHVtZSIsIm9yZGVyX3R5cGUiOiJEZXNjIiwibmV4dCI6bnVsbH0sImxpbWl0IjoxLCJvZmZzZXQiOjAsImFpZCI6MTUzNX0sIlJhd1F1ZXJ5IjpudWxsLCJJZCI6Ijc0MjcwOGQwLWZjMjgtNDMwZi04NzA3LTRhZmVjYmJkNDgwZCIsIlNlYXJjaEFmdGVyRGF0YSI6WzE4MzAwMDAsIjkwYzI4YjVjLWVmNWQtNGUwMi04MGU2LTBkYThkZjQyZDY0NyJdfQ==",\
"items": [\
{\
"se_type": "google",\
"keyword": "boost cell phone",\
"location_code": 2840,\
"language_code": "en",\
"keyword_info": {\
"se_type": "google",\
"last_updated_time": "2024-08-12 23:31:45 +00:00",\
"competition": 0.96,\
"competition_level": "HIGH",\
"cpc": 1.47,\
"search_volume": 1830000,\
"low_top_of_page_bid": 0.85,\
"high_top_of_page_bid": 10.44,\
"categories": [\
10007,\
10878,\
12161,\
13381\
],\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 2240000\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 2240000\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 1830000\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 1830000\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 2240000\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 1830000\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 1830000\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 2240000\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 2240000\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 1830000\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 1830000\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 1830000\
}\
],\
"search_volume_trend": {\
"monthly": 22,\
"quarterly": 22,\
"yearly": 0\
}\
},\
"clickstream_keyword_info": null,\
"keyword_properties": {\
"se_type": "google",\
"core_keyword": null,\
"synonym_clustering_algorithm": "text_processing",\
"keyword_difficulty": 0,\
"detected_language": "en",\
"is_another_language": false\
},\
"serp_info": {\
"se_type": "google",\
"check_url": "https://www.google.com/search?q=boost%20cell%20phone&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",\
"serp_item_types": [\
"organic",\
"people_also_ask",\
"local_pack",\
"popular_products",\
"top_sights",\
"video",\
"images",\
"related_searches"\
],\
"se_results_count": 115000000,\
"last_updated_time": "2024-08-04 08:25:36 +00:00",\
"previous_updated_time": "2024-06-22 17:54:36 +00:00"\
},\
"avg_backlinks_info": {\
"se_type": "google",\
"backlinks": 4739.3,\
"dofollow": 2334.9,\
"referring_pages": 4121.3,\
"referring_domains": 210.3,\
"referring_main_domains": 184.2,\
"rank": 113.1,\
"main_domain_rank": 512.4,\
"last_updated_time": "2024-08-04 08:25:38 +00:00"\
},\
"search_intent_info": {\
"se_type": "google",\
"main_intent": "transactional",\
"foreign_intent": null,\
"last_updated_time": "2023-12-14 04:27:21 +00:00"\
},\
"keyword_info_normalized_with_bing": {\
"last_updated_time": "2024-08-17 06:05:32 +00:00",\
"search_volume": 2893,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 3541\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 3541\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 2893\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 2893\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 3541\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 2893\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 2893\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 3541\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 3541\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 2893\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 2893\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 2893\
},\
{\
"year": 2023,\
"month": 7,\
"search_volume": 2778\
}\
]\
},\
"keyword_info_normalized_with_clickstream": {\
"last_updated_time": "2024-08-17 06:05:32 +00:00",\
"search_volume": 197,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 242\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 242\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 197\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 197\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 242\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 197\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 197\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 242\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 242\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 197\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 197\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 197\
},\
{\
"year": 2023,\
"month": 7,\
"search_volume": 190\
}\
]\
}\
}\
]\
}\
]\
}\
]
}
```
**`POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live`**
Your account will be charged for each request.
The cost can be calculated on the [Pricing](https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api "Pricing") page.
All POST data should be sent in the [JSON](https://en.wikipedia.org/wiki/JSON) format (UTF-8 encoding). The task setting is done using the POST method. When setting a task, you should send all task parameters in the task array of the generic POST array. You can send up to 2000 API calls per minute. The maximum number of requests that can be sent simultaneously is limited to 30.
You can specify the number of results you want to retrieve, filter and sort them.
Below you will find a detailed description of the fields you can use for setting a task.
**Description of the fields for setting a task:**
| Field name | Type | Description |
| --- | --- | --- |
| `keyword` | string | _keyword_
**required field**
UTF-8 encoding
the keywords will be converted to lowercase format;
learn more about rules and limitations of `keyword` and `keywords` fields in DataForSEO APIs in this [Help Center article](https://dataforseo.com/help-center/rules-and-limitations-of-keyword-and-keywords-fields-in-dataforseo-apis) | |
| `location_name` | string | _full name of the location_
optional field
if you use this field, you don’t need to specify `location_code`
you can receive the list of available locations with their `location_name` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
ignore this field to get the results for all available locations
example:
`United Kingdom` | |
| `location_code` | integer | _location code_
optional field
if you use this field, you don’t need to specify `location_name`
you can receive the list of available locations with their `location_code` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
ignore this field to get the results for all available locations
example:
`2840` | |
| `language_name` | string | _full name of the language_
optional field
if you use this field, you don’t need to specify `language_code`
you can receive the list of available languages with their `language_name` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`English`
**Note:** if omitted, results default to the language with the most keyword records in the specified location;
refer to the `available_languages.keywords` field of the [Locations and Languages endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages) to determine the default language | |
| `language_code` | string | _language code_
optional field
if you use this field, you don’t need to specify `language_name`
you can receive the list of available languages with their `language_code` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`en`
**Note:** if omitted, results default to the language with the most keyword records in the specified location;
refer to the `available_languages.keywords` field of the [Locations and Languages endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages) to determine the default language | |
| `include_seed_keyword` | boolean | _include data for the seed keyword_
optional field
if set to `true`, data for the seed keyword specified in the `keyword` field will be provided in the `seed_keyword_data` array of the response
default value: `false` | |
| `include_serp_info` | boolean | _include data from SERP for each keyword_
optional field
if set to `true`, we will return a `serp_info` array containing SERP data (number of search results, relevant URL, and SERP features) for every keyword in the response
default value: `false` | |
| `include_clickstream_data` | boolean | _include or exclude data from clickstream-based metrics in the result_
optional field
if the parameter is set to `true`, you will receive `clickstream_keyword_info`, `keyword_info_normalized_with_clickstream`, and `keyword_info_normalized_with_bing` fields in the response
default value: `false`
with this parameter enabled, you will be charged double the price for the request
learn more about how clickstream-based metrics are calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `exact_match` | boolean | _search for the exact phrase_
optional field
if set to `true`, the returned keywords will include the exact keyword phrase you specified, with potentially other words before or after that phrase
default value: `false` | |
| `ignore_synonyms` | boolean | _ignore highly similar keywords_
optional field
if set to `true` only core keywords will be returned, all highly similar keywords will be excluded;
default value: `false` | |
| `filters` | array | _array of results filtering parameters_
optional field
**you can add several filters at once (8 filters maximum)**
you should set a logical operator `and`, `or` between the conditions
the following operators are supported:
`regex`, `not_regex`, `<`, `<=`, `>`, `>=`, `=`, `<>`, `in`, `not_in`, `match`, `not_match`, `ilike`, `not_ilike`, `like`, `not_like`
you can use the `%` operator with `like` and `not_like`, as well as `ilike` and `not_ilike` to match any string of zero or more characters
example:
`["keyword_info.search_volume",">",0]`
`[["keyword_info.search_volume","in",[0,1000]],
"and",
["keyword_info.competition_level","=","LOW"]]` `[["keyword_info.search_volume",">",100],
"and",
[["keyword_info.cpc","<",0.5],
"or",
["keyword_info.high_top_of_page_bid","<=",0.5]]]`
for more information about filters, please refer to [Dataforseo Labs – Filters](https://docs.dataforseo.com/v3/dataforseo_labs/filters) or this [help center guide](https://dataforseo.com/help-center/how-to-use-filters-in-dataforseo-labs-api) | |
| `order_by` | array | _results sorting rules_
optional field
you can use the same values as in the `filters` array to sort the results
possible sorting types:
`asc` – results will be sorted in the ascending order
`desc` – results will be sorted in the descending order
a comma is used as a separator
example:
`["keyword_info.competition,desc"]`
default rule:
`["keyword_info.search_volume,desc"]`
**note that you can set no more than three sorting rules in a single request**
you should use a comma to separate several sorting rules
example:
`["keyword_info.search_volume,desc","keyword_info.cpc,desc"]` | |
| `limit` | integer | _the maximum number of returned keywords_
optional field
default value: `100`
maximum value: `1000` | |
| `offset` | integer | _offset in the results array of returned keywords_
optional field
default value: `0`
if you specify the `10` value, the first ten keywords in the results array will be omitted and the data will be provided for the successive keywords | |
| `offset_token` | string | _offset token for subsequent requests_
optional field
provided in the identical filed of the response to each request;
use this parameter to avoid timeouts while trying to obtain over 10,000 results in a single request;
by specifying the unique `offset_token` value from the response array, you will get the subsequent results of the initial task;
`offset_token` values are unique for each subsequent task
**Note:** if the `offset_token` is specified in the request, all other parameters except `limit` will not be taken into account when processing a task. | |
| `tag` | string | _user-defined task identifier_
optional field
_the character limit is 255_
you can use this parameter to identify the task and match it with the result
you will find the specified `tag` value in the `data` object of the response | |
‌
As a response of the API server, you will receive [JSON](https://en.wikipedia.org/wiki/JSON)-encoded data containing a `tasks` array with the information specific to the set tasks.
**Description of the fields in the results array:**
| Field name | Type | Description |
| --- | --- | --- |
| `version` | string | _the current version of the API_ | |
| `status_code` | integer | _general status code_
you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors)
**Note:** we strongly recommend designing a necessary system for handling related exceptional or error conditions | |
| `status_message` | string | _general informational message_
you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) | |
| `time` | string | _execution time, seconds_ | |
| `cost` | float | _total tasks cost, USD_ | |
| `tasks_count` | integer | _the number of tasks in the **`tasks`** array_ | |
| `tasks_error` | integer | _the number of tasks in the **`tasks`** array returned with an error_ | |
| **`tasks`** | array | _array of tasks_ | |
| `id` | string | _task identifier_
**unique task identifier in our system in the [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format** | |
| `status_code` | integer | _status code of the task_
generated by DataForSEO; can be within the following range: 10000-60000
you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) | |
| `status_message` | string | _informational message of the task_
you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix-errors/) | |
| `time` | string | _execution time, seconds_ | |
| `cost` | float | _cost of the task, USD_ | |
| `result_count` | integer | _number of elements in the `result` array_ | |
| `path` | array | _URL path_ | |
| `data` | object | _contains the same parameters that you specified in the POST request_ | |
| **`result`** | array | _array of results_ | |
| `se_type` | string | _search engine type_ | |
| `seed_keyword` | string | _keyword in a POST array_ | |
| **`seed_keyword_data`** | object | _keyword data for the seed keyword_
fields in this object are identical to those of the `items` array | |
| `location_code` | integer | _location code in a POST array_
if there is no data, then the value is `null` | |
| `language_code` | string | _language code in a POST array_
if there is no data, then the value is `null` | |
| `total_count` | integer | _total amount of results in our database relevant to your request_ | |
| `items_count` | integer | _the number of results returned in the `items` array_ | |
| `offset` | integer | _current offset value_ | |
| `offset_token` | string | _offset token for subsequent requests_
you can use the string provided in this field to get the subsequent results of the initial task;
**note:** `offset_token` values are unique for each subsequent task | |
| **`items`** | array | _contains keywords and related data_ | |
| `se_type` | string | _search engine type_ | |
| `keyword` | string | _keyword suggestion_ | |
| `location_code` | integer | _location code in a POST array_ | |
| `language_code` | string | _language code in a POST array_ | |
| **`keyword_info`** | object | _keyword data for the returned keyword_ | |
| `se_type` | string | _search engine type_ | |
| `last_updated_time` | string | _date and time when keyword data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `competition` | float | _competition_
represents the relative amount of competition associated with the given keyword;
the value is based on Google Ads data and can be between 0 and 1 (inclusive) | |
| `competition_level` | string | _competition level_
represents the relative level of competition associated with the given keyword in paid SERP only;
possible values: `LOW`, `MEDIUM`, `HIGH`
if competition level is unknown, the value is `null`;
learn more about the metric in [this help center article](https://dataforseo.com/help-center/what-is-competition) | |
| `cpc` | float | _cost-per-click_
represents the average cost per click (USD) historically paid for the keyword | |
| `search_volume` | integer | _average monthly search volume rate_
represents the (approximate) number of searches for the given keyword idea on google.com | |
| `low_top_of_page_bid` | float | _minimum bid for the ad to be displayed at the top of the first page_
indicates the value greater than about 20% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)
the value may differ depending on the location specified in a POST request | |
| `high_top_of_page_bid` | float | _maximum bid for the ad to be displayed at the top of the first page_
indicates the value greater than about 80% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)
the value may differ depending on the location specified in a POST request | |
| `categories` | array | _product and service categories_
you can download the [full list of possible categories](https://cdn.dataforseo.com/v3/categories/categories_dataforseo_labs_2023_10_25.csv) | |
| `monthly_searches` | array | _monthly searches_
represents the (approximate) number of searches for this keyword idea (as available for the past twelve months), targeted to the specified geographic locations | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _monthly average search volume rate_ | |
| `search_volume_trend` | object | _search volume trend changes_
represents search volume change in percent compared to the previous period | |
| `monthly` | integer | _search volume change in percent compared to the previous month_ | |
| `quarterly` | integer | _search volume change in percent compared to the previous quarter_ | |
| `yearly` | integer | _search volume change in percent compared to the previous year_ | |
| `clickstream_keyword_info` | object | _clickstream data for the returned keyword_
to retrieve results for this field, the parameter `include_clickstream_data` must be set to `true` | |
| `search_volume` | integer | _monthly average clickstream search volume rate_ | |
| `last_updated_time` | string | _date and time when the clickstream dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” | |
| `gender_distribution` | object | _distribution of estimated clickstream-based metrics by gender_
learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `female` | integer | _number of female users in the relevant clickstream dataset_ | |
| `male` | integer | _number of male users in the relevant clickstream dataset_ | |
| `age_distribution` | object | _distribution of clickstream-based metrics by age_
learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `18-24` | integer | _number of users in the relevant clickstream dataset that fall within the 18-24 age range_ | |
| `25-34` | integer | _number of users in the relevant clickstream dataset that fall within the 25-34 age range_ | |
| `35-44` | integer | _number of users in the relevant clickstream dataset that fall within the 35-44 age range_ | |
| `45-54` | integer | _number of users in the relevant clickstream dataset that fall within the 45-54 age range_ | |
| `55-64` | integer | _number of users in the relevant clickstream dataset that fall within the 55-64 age range_ | |
| `monthly_searches` | array | _monthly clickstream search volume rates_
array of objects with clickstream search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _clickstream-based search volume rate in a certain month of a year_ | |
| **`keyword_properties`** | object | _additional information about the keyword_ | |
| `se_type` | string | _search engine type_ | |
| `core_keyword` | string | _main keyword in a group_
contains the main keyword in a group determined by the synonym clustering algorithm
if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` | |
| `synonym_clustering_algorithm` | string | _the algorithm used to identify synonyms_
possible values:
`keyword_metrics` – indicates the algorithm based on `keyword_info` parameters
`text_processing` – indicates the text-based algorithm
if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` | |
| `keyword_difficulty` | integer | _difficulty of ranking in the first top-10 organic results for a keyword_
indicates the chance of getting in top-10 organic results for a keyword on a logarithmic scale from 0 to 100;
calculated by analysing, among other parameters, link profiles of the first 10 pages in SERP;
learn more about the metric in [this help center guide](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated) | |
| `detected_language` | string | _detected language of the keyword_
indicates the language of the keyword as identified by our system | |
| `is_another_language` | boolean | _detected language of the keyword is different from the set language_
if `true`, the language set in the request does not match the language determined by our system for a given keyword | |
| **`serp_info`** | object | _SERP data_
the value will be `null` if you didn’t set the field `include_serp_info` to `true` in the POST array or if there is no SERP data for this keyword in our database | |
| `se_type` | string | _search engine type_ | |
| `check_url` | string | _direct URL to search engine results_
you can use it to make sure that we provided accurate results | |
| `serp_item_types` | array | _types of search results in SERP_
contains types of search results (items) found in SERP
possible item types:
`answer_box`, `app`, `carousel`, `multi_carousel`, `featured_snippet`, `google_flights`, `google_reviews`, `third_party_reviews`, `google_posts`, `images`, `jobs`, `knowledge_graph`, `local_pack`, `hotels_pack`, `map`, `organic`, `paid`, `people_also_ask`, `related_searches`, `people_also_search`, `shopping`, `top_stories`, `twitter`, `video`, `events`, `mention_carousel`, `recipes`, `top_sights`, `scholarly_articles`, `popular_products`, `podcasts`, `questions_and_answers`, `find_results_on`, `stocks_box`, `visual_stories`, `commercial_units`, `local_services`, `google_hotels`, `math_solver`, `currency_box`, `product_considerations`, `found_on_web`, `short_videos`, `refine_products`, `explore_brands`, `perspectives`, `discussions_and_forums`, `compare_sites`, `courses`, `ai_overview`;
**note** that the actual results will be returned only for `organic`, `paid`, `featured_snippet`, and `local_pack` elements | |
| `se_results_count` | string | _number of search results for the returned keyword_ | |
| `last_updated_time` | string | _date and time when SERP data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `previous_updated_time` | string | _previous to the most recent date and time when SERP data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-10-15 12:57:46 +00:00` | |
| **`avg_backlinks_info`** | object | _backlink data for the returned keyword_
this object provides the average number of backlinks, referring pages and domains, as well as the average rank values among the top-10 webpages ranking organically for the keyword | |
| `se_type` | string | _search engine type_ | |
| `backlinks` | float | _average number of backlinks_ | |
| `dofollow` | float | _average number of dofollow links_ | |
| `referring_pages` | float | _average number of referring pages_ | |
| `referring_domains` | float | _average number of referring domains_ | |
| `referring_main_domains` | float | _average number of referring main domains_ | |
| `rank` | float | _average rank_
learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) | |
| `main_domain_rank` | float | _average main domain rank_
learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) | |
| `last_updated_time` | string | _date and time when backlink data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| **`search_intent_info`** | object | _search intent info for the returned keyword_
learn about search intent in this [help center article](https://dataforseo.com/help-center/search-intent-and-its-types) | |
| `se_type` | string | _search engine type_
possible values: `google` | |
| `main_intent` | string | _main search intent_
possible values: `informational`, `navigational`, `commercial`, `transactional` | |
| `foreign_intent` | array | _supplementary search intents_
possible values: `informational`, `navigational`, `commercial`, `transactional` | |
| `last_updated_time` | string | _date and time when search intent data was last updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| **`keyword_info_normalized_with_bing`** | object | _contains keyword search volume normalized with Bing search volume_ | |
| `last_updated_time` | string | _date and time when the dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `search_volume` | integer | _current search volume rate of a keyword_ | |
| `is_normalized` | boolean | _keyword info is normalized_
if `true`, values are normalized with Bing data | |
| `monthly_searches` | integer | _monthly search volume rates_
array of objects with search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _search volume rate in a certain month of a year_ | |
| **`keyword_info_normalized_with_clickstream`** | object | _contains keyword search volume normalized with clickstream data_ | |
| `last_updated_time` | string | _date and time when the dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `search_volume` | integer | _current search volume rate of a keyword_ | |
| `is_normalized` | boolean | _keyword info is normalized_
if `true`, values are normalized with clickstream data | |
| `monthly_searches` | integer | _monthly search volume rates_
array of objects with search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _search volume rate in a certain month of a year_ | |
‌‌
[cURL](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live/?bash#) [php](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live/?bash#) [NodeJs](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live/?bash#) [Python](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live/?bash#) [cSharp](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live/?bash#)
## Related Keywords
The Related Keywords endpoint provides keywords appearing in the
["searches related to" SERP element![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-related-searches.png)](https://docs.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live/?bash#)
You can get up to 4680 keyword ideas by specifying the search depth. Each related keyword comes with the list of relevant product categories, search volume rate for the last month, search volume trend for the previous 12 months, as well as current cost-per-click and competition values.
**Datasource:** DataForSEO SERPs Database
**Search algorithm:** depth-first search for queries appearing in the “search related to” element of SERP for the specified seed keyword.
**Examples:**
Note: the `depth` parameter is set to `1`
Specified seed keyword:
_“keyword research”_
Resulting related keywords:
_•”free keyword research”_,
_•”keyword research tools”_,
_•”best free keyword research tool”_,
_•”keyword research tips”_,
_•”seo keyword research tool”_,
_•”keyword research step by step”_,
_•”how to do keyword research 2019″_,
_•”keyword research google ads”_
> Instead of ‘login’ and ‘password’ use your credentials from https://app.dataforseo.com/api-access
```
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"
curl --location --request POST "https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json" \
--data-raw '[\
{\
"keyword": "phone",\
"language_name": "English",\
"location_code": 2840,\
"limit": 3\
}\
]'
```
```
// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip
require('RestClient.php');
$api_url = 'https://api.dataforseo.com/';
// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
$client = new RestClient($api_url, null, 'login', 'password');
$post_array = array();
// simple way to set a task
$post_array[] = array(
"keyword" => "phone",
"language_name" => "English",
"location_code" => 2840,
"filters" => [\
["keyword_data.keyword_info.search_volume", ">", 10]\
],
"limit": 3
);
try {
// POST /v3/dataforseo_labs/google/related_keywords/live
$result = $client->post('/v3/dataforseo_labs/google/related_keywords/live', $post_array);
print_r($result);
// do something with post result
} catch (RestClientException $e) {
echo "n";
print "HTTP code: {$e->getHttpCode()}n";
print "Error code: {$e->getCode()}n";
print "Message: {$e->getMessage()}n";
print $e->getTraceAsString();
echo "n";
}
$client = null;
?>
```
```
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
keyword="phone",
location_name="United States",
language_name="English",
filters=[\
["keyword_data.keyword_info.search_volume", ">", 10]\
],
limit=3
)
# POST /v3/dataforseo_labs/google/related_keywords/live
response = client.post("/v3/dataforseo_labs/google/related_keywords/live", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
print(response)
# do something with result
else:
print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
```
```
const post_array = [];
post_array.push({
"keyword": "phone",
"language_name": "English",
"location_code": 2840,
"filters": [\
["keyword_data.keyword_info.search_volume", ">", 10]\
],
"limit": 3
});
const axios = require('axios');
axios({
method: 'post',
url: 'https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live',
auth: {
username: 'login',
password: 'password'
},
data: post_array,
headers: {
'content-type': 'application/json'
}
}).then(function (response) {
var result = response['data']['tasks'];
// Result data
console.log(result);
}).catch(function (error) {
console.log(error);
});
```
```
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
namespace DataForSeoDemos
{
public static partial class Demos
{
public static async Task dataforseo_labs_google_related_keywords_live()
{
var httpClient = new HttpClient
{
BaseAddress = new Uri("https://api.dataforseo.com/"),
// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
};
var postData = new List();
postData.Add(new
{
keyword = "phone",
location_name = "United States",
language_name = "English",
filters = new object[]
{
new object[] { "keyword_data.keyword_info.search_volume", ">", 10 }
},
limit = 3
});
// POST /v3/dataforseo_labs/google/related_keywords/live
// the full list of possible parameters is available in documentation
var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/related_keywords/live", new StringContent(JsonConvert.SerializeObject(postData)));
var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());
// you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if (result.status_code == 20000)
{
// do something with result
Console.WriteLine(result);
}
else
Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");
}
}
}
```
> The above command returns JSON structured like this:
```
{
"version": "0.1.20240801",
"status_code": 20000,
"status_message": "Ok.",
"time": "0.0995 sec.",
"cost": 0.0103,
"tasks_count": 1,
"tasks_error": 0,
"tasks": [\
{\
"id": "08221812-1535-0387-0000-53d53d3e60c5",\
"status_code": 20000,\
"status_message": "Ok.",\
"time": "0.0326 sec.",\
"cost": 0.0103,\
"result_count": 1,\
"path": [\
"v3",\
"dataforseo_labs",\
"google",\
"related_keywords",\
"live"\
],\
"data": {\
"api": "dataforseo_labs",\
"function": "related_keywords",\
"se_type": "google",\
"keyword": "phone",\
"language_name": "English",\
"location_code": 2840,\
"limit": 3\
},\
"result": [\
{\
"se_type": "google",\
"seed_keyword": "phone",\
"seed_keyword_data": null,\
"location_code": 2840,\
"language_code": "en",\
"total_count": 9,\
"items_count": 3,\
"items": [\
{\
"se_type": "google",\
"keyword_data": {\
"se_type": "google",\
"keyword": "phone",\
"location_code": 2840,\
"language_code": "en",\
"keyword_info": {\
"se_type": "google",\
"last_updated_time": "2024-08-11 13:24:34 +00:00",\
"competition": 1,\
"competition_level": "HIGH",\
"cpc": 5.98,\
"search_volume": 368000,\
"low_top_of_page_bid": 3.08,\
"high_top_of_page_bid": 10.5,\
"categories": [\
10007,\
10878,\
12133,\
13381\
],\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 450000\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 368000\
}\
],\
"search_volume_trend": {\
"monthly": 22,\
"quarterly": 22,\
"yearly": 0\
}\
},\
"clickstream_keyword_info": null,\
"keyword_properties": {\
"se_type": "google",\
"core_keyword": null,\
"synonym_clustering_algorithm": "text_processing",\
"keyword_difficulty": 83,\
"detected_language": "en",\
"is_another_language": false\
},\
"serp_info": {\
"se_type": "google",\
"check_url": "https://www.google.com/search?q=phone&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",\
"serp_item_types": [\
"popular_products",\
"images",\
"organic",\
"product_considerations",\
"refine_products",\
"top_stories",\
"related_searches"\
],\
"se_results_count": 19880000000,\
"last_updated_time": "2024-07-15 00:43:34 +00:00",\
"previous_updated_time": "2024-05-18 22:29:28 +00:00"\
},\
"avg_backlinks_info": {\
"se_type": "google",\
"backlinks": 6835.7,\
"dofollow": 3775.6,\
"referring_pages": 5352.2,\
"referring_domains": 1100.3,\
"referring_main_domains": 955.1,\
"rank": 369.3,\
"main_domain_rank": 681.2,\
"last_updated_time": "2024-07-14 21:43:39 +00:00"\
},\
"search_intent_info": {\
"se_type": "google",\
"main_intent": "navigational",\
"foreign_intent": [\
"commercial"\
],\
"last_updated_time": "2023-03-02 03:54:21 +00:00"\
},\
"keyword_info_normalized_with_bing": {\
"last_updated_time": "2024-08-17 01:41:37 +00:00",\
"search_volume": 324416,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 396705\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 324416\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 324416\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 324416\
}\
]\
},\
"keyword_info_normalized_with_clickstream": {\
"last_updated_time": "2024-08-11 13:24:34 +00:00",\
"search_volume": 368000,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 450000\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 368000\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 368000\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 368000\
}\
]\
}\
},\
"depth": 0,\
"related_keywords": [\
"phone app",\
"phone call",\
"phone app download",\
"phone call app",\
"phone samsung",\
"phone definition",\
"phone app on android",\
"my phone app"\
]\
},\
{\
"se_type": "google",\
"keyword_data": {\
"se_type": "google",\
"keyword": "phone call",\
"location_code": 2840,\
"language_code": "en",\
"keyword_info": {\
"se_type": "google",\
"last_updated_time": "2024-08-08 14:16:10 +00:00",\
"competition": 0.07,\
"competition_level": "LOW",\
"cpc": 4.23,\
"search_volume": 27100,\
"low_top_of_page_bid": 0.92,\
"high_top_of_page_bid": 7.55,\
"categories": [\
10007,\
10019,\
10167,\
10878,\
11506,\
11510,\
12762,\
13419\
],\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 60500\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 27100\
}\
],\
"search_volume_trend": {\
"monthly": 22,\
"quarterly": 22,\
"yearly": 0\
}\
},\
"clickstream_keyword_info": null,\
"keyword_properties": {\
"se_type": "google",\
"core_keyword": "phone calling",\
"synonym_clustering_algorithm": "text_processing",\
"keyword_difficulty": 57,\
"detected_language": "en",\
"is_another_language": false\
},\
"serp_info": {\
"se_type": "google",\
"check_url": "https://www.google.com/search?q=phone%20call&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",\
"serp_item_types": [\
"organic",\
"people_also_ask",\
"related_searches"\
],\
"se_results_count": 25270000000,\
"last_updated_time": "2024-08-04 13:21:19 +00:00",\
"previous_updated_time": "2024-06-22 22:50:34 +00:00"\
},\
"avg_backlinks_info": {\
"se_type": "google",\
"backlinks": 11475.1,\
"dofollow": 7174.8,\
"referring_pages": 10754.1,\
"referring_domains": 884.2,\
"referring_main_domains": 765,\
"rank": 329.4,\
"main_domain_rank": 787.5,\
"last_updated_time": "2024-08-04 10:21:19 +00:00"\
},\
"search_intent_info": {\
"se_type": "google",\
"main_intent": "commercial",\
"foreign_intent": null,\
"last_updated_time": "2023-03-02 03:54:30 +00:00"\
},\
"keyword_info_normalized_with_bing": {\
"last_updated_time": "2024-08-16 12:35:38 +00:00",\
"search_volume": 19134,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 19134\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 42717\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 19134\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 19134\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 19134\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 19134\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 19134\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 19134\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 19134\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 19134\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 19134\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 19134\
}\
]\
},\
"keyword_info_normalized_with_clickstream": {\
"last_updated_time": "2024-08-08 14:16:10 +00:00",\
"search_volume": 27100,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 60500\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 27100\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 27100\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 27100\
}\
]\
}\
},\
"depth": 1,\
"related_keywords": [\
"phone call online",\
"phone call app",\
"free phone call",\
"phone app",\
"phone call app download",\
"i want to make a phone call on my phone",\
"phone by google",\
"make a phone call to someone"\
]\
},\
{\
"se_type": "google",\
"keyword_data": {\
"se_type": "google",\
"keyword": "phone app",\
"location_code": 2840,\
"language_code": "en",\
"keyword_info": {\
"se_type": "google",\
"last_updated_time": "2024-08-11 20:06:52 +00:00",\
"competition": 0.15,\
"competition_level": "LOW",\
"cpc": 2.14,\
"search_volume": 22200,\
"low_top_of_page_bid": 0.46,\
"high_top_of_page_bid": 3.16,\
"categories": [\
10007,\
10019,\
10168,\
10878,\
10885,\
13378,\
13381\
],\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 22200\
}\
],\
"search_volume_trend": {\
"monthly": 22,\
"quarterly": 22,\
"yearly": 0\
}\
},\
"clickstream_keyword_info": null,\
"keyword_properties": {\
"se_type": "google",\
"core_keyword": "phone for apps",\
"synonym_clustering_algorithm": "text_processing",\
"keyword_difficulty": 66,\
"detected_language": "en",\
"is_another_language": false\
},\
"serp_info": {\
"se_type": "google",\
"check_url": "https://www.google.com/search?q=phone%20app&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",\
"serp_item_types": [\
"organic",\
"people_also_ask",\
"images",\
"related_searches"\
],\
"se_results_count": 25270000000,\
"last_updated_time": "2024-08-04 13:51:15 +00:00",\
"previous_updated_time": "2024-06-22 23:19:03 +00:00"\
},\
"avg_backlinks_info": {\
"se_type": "google",\
"backlinks": 4502.4,\
"dofollow": 2513.9,\
"referring_pages": 3667.1,\
"referring_domains": 984.5,\
"referring_main_domains": 855.8,\
"rank": 322.6,\
"main_domain_rank": 814.6,\
"last_updated_time": "2024-08-04 10:51:22 +00:00"\
},\
"search_intent_info": {\
"se_type": "google",\
"main_intent": "commercial",\
"foreign_intent": [\
"navigational"\
],\
"last_updated_time": "2023-03-02 03:54:24 +00:00"\
},\
"keyword_info_normalized_with_bing": {\
"last_updated_time": "2024-08-16 23:26:54 +00:00",\
"search_volume": 4979,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 4979\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 4979\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 4979\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 4979\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 4979\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 4979\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 4979\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 4979\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 4979\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 4979\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 4979\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 4979\
}\
]\
},\
"keyword_info_normalized_with_clickstream": {\
"last_updated_time": "2024-08-11 20:06:52 +00:00",\
"search_volume": 22200,\
"is_normalized": true,\
"monthly_searches": [\
{\
"year": 2024,\
"month": 7,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 6,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 5,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 4,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 3,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 2,\
"search_volume": 22200\
},\
{\
"year": 2024,\
"month": 1,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 12,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 11,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 10,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 9,\
"search_volume": 22200\
},\
{\
"year": 2023,\
"month": 8,\
"search_volume": 22200\
}\
]\
}\
},\
"depth": 1,\
"related_keywords": [\
"phone app download",\
"phone app on android",\
"my phone app",\
"phone app free",\
"google phone app",\
"phone call",\
"phone app download free",\
"phone by google"\
]\
}\
]\
}\
]\
}\
]
}
```
**`POST https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live`**
Your account will be charged for each request.
The cost can be calculated on the [Pricing](https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api "Pricing") page.
All POST data should be sent in the [JSON](https://en.wikipedia.org/wiki/JSON) format (UTF-8 encoding). The task setting is done using the POST method. When setting a task, you should send all task parameters in the task array of the generic POST array. You can send up to 2000 API calls per minute. The maximum number of requests that can be sent simultaneously is limited to 30.
You can specify the number of results you want to retrieve, filter and sort them.
Below you will find a detailed description of the fields you can use for setting a task.
**Description of the fields for setting a task:**
| Field name | Type | Description |
| --- | --- | --- |
| `keyword` | string | _keyword_
**required field**
UTF-8 encoding
the keywords will be converted to lowercase format
learn more about rules and limitations of `keyword` and `keywords` fields in DataForSEO APIs in this [Help Center article](https://dataforseo.com/help-center/rules-and-limitations-of-keyword-and-keywords-fields-in-dataforseo-apis) | |
| `location_name` | string | _full name of the location_
**required field if you don’t specify** `location_code`
**Note:** it is required to specify either `location_name` or `location_code`
you can receive the list of available locations with their `location_name` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`United Kingdom` | |
| `location_code` | integer | _location code_
**required field if you don’t specify** `location_name`
**Note:** it is required to specify either `location_name` or `location_code`
you can receive the list of available locations with their `location_code` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`2840` | |
| `language_name` | string | _full name of the language_
**required field if you don’t specify** `language_code`
**Note:** it is required to specify either `language_name` or `language_code`
you can receive the list of available locations with their `language_name` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`English` | |
| `language_code` | string | _language code_
**required field if you don’t specify** `language_name`
**Note:** it is required to specify either `language_name` or `language_code`
you can receive the list of available locations with their `language_code` by making a separate request to the
`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`
example:
`en` | |
| `depth` | integer | _keyword search depth_
optional field
default value: `1`
number of the returned results depends on the value you set in this field
you can specify a level from 0 to 4
estimated number of keywords for each level (maximum):
0 – the keyword set in the `keyword` field
1 – 8 keywords
2 – 72 keywords
3 – 584 keywords
4 – 4680 keywords | |
| `include_seed_keyword` | boolean | _include data for the seed keyword_
optional field
if set to `true`, data for the seed keyword specified in the `keyword` field will be provided in the `seed_keyword_data` array of the response
default value: `false` | |
| `include_serp_info` | boolean | _include data from SERP for each keyword_
optional field
if set to `true`, we will return a `serp_info` array containing SERP data (number of search results, relevant URL, and SERP features) for every keyword in the response
default value: `false` | |
| `include_clickstream_data` | boolean | _include or exclude data from clickstream-based metrics in the result_
optional field
if the parameter is set to `true`, you will receive `clickstream_keyword_info`, `keyword_info_normalized_with_clickstream`, and `keyword_info_normalized_with_bing` fields in the response
default value: `false`
with this parameter enabled, you will be charged double the price for the request
learn more about how clickstream-based metrics are calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `ignore_synonyms` | boolean | _ignore highly similar keywords_
optional field
if set to `true` only core keywords will be returned, all highly similar keywords will be excluded;
default value: `false` | |
| `replace_with_core_keyword` | boolean | _return data for core keyword_
optional field
if `true`, `serp_info` and `related_keywords` will be returned for the main keyword in the group that the specified `keyword` belongs to;
if `false`, `serp_info` and `related_keywords` will be returned for the specified `keyword` (if available);
refer to [this help center article](https://dataforseo.com/help-center/replace_with_core_keyword) for more details;
default value: `false` | |
| `filters` | array | _array of results filtering parameters_
optional field
**you can add several filters at once (8 filters maximum)**
you should set a logical operator `and`, `or` between the conditions
the following operators are supported:
`regex`, `not_regex`, `<`, `<=`, `>`, `>=`, `=`, `<>`, `in`, `not_in`, `match`, `not_match`, `ilike`, `not_ilike`, `like`, `not_like`
you can use the `%` operator with `like` and `not_like`, as well as `ilike` and `not_ilike` to match any string of zero or more characters
example:
`["keyword_data.keyword_info.search_volume",">",0]`
`[["keyword_info.search_volume","in",[0,1000]],
"and",
["keyword_data.keyword_info.competition_level","=","LOW"]]`
`[["keyword_data.keyword_info.search_volume",">",100],
"and",
[["keyword_data.keyword_info.cpc","<",0.5],
"or",
["keyword_info.high_top_of_page_bid","<=",0.5]]]`
for more information about filters, please refer to [Dataforseo Labs – Filters](https://docs.dataforseo.com/v3/dataforseo_labs/filters) or this [help center guide](https://dataforseo.com/help-center/how-to-use-filters-in-dataforseo-labs-api) | |
| `order_by` | array | _results sorting rules_
optional field
you can use the same values as in the `filters` array to sort the results
possible sorting types:
`asc` – results will be sorted in the ascending order
`desc` – results will be sorted in the descending order
you should use a comma to set up a sorting type
example:
`["keyword_data.keyword_info.competition,desc"]`
default rule:
`["keyword_data.keyword_info.search_volume,desc"]`
**note that you can set no more than three sorting rules in a single request**
you should use a comma to separate several sorting rules
example:
`["keyword_data.keyword_info.search_volume,desc","keyword_data.keyword_info.cpc,desc"]` | |
| `limit` | integer | _the maximum number of returned keywords_
optional field
default value: `100`
maximum value: `1000` | |
| `offset` | integer | _offset in the results array of returned keywords_
optional field
default value: `0`
if you specify the `10` value, the first ten keywords in the results array will be omitted and the data will be provided for the successive keywords | |
| `tag` | string | _user-defined task identifier_
optional field
_the character limit is 255_
you can use this parameter to identify the task and match it with the result
you will find the specified `tag` value in the `data` object of the response | |
‌
As a response of the API server, you will receive [JSON](https://en.wikipedia.org/wiki/JSON)-encoded data containing a `tasks` array with the information specific to the set tasks.
**Description of the fields in the results array:**
| Field name | Type | Description |
| --- | --- | --- |
| `version` | string | _the current version of the API_ | |
| `status_code` | integer | _general status code_
you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors)
**Note:** we strongly recommend designing a necessary system for handling related exceptional or error conditions | |
| `status_message` | string | _general informational message_
you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) | |
| `time` | string | _execution time, seconds_ | |
| `cost` | float | _total tasks cost, USD_ | |
| `tasks_count` | integer | _the number of tasks in the **`tasks`** array_ | |
| `tasks_error` | integer | _the number of tasks in the **`tasks`** array returned with an error_ | |
| **`tasks`** | array | _array of tasks_ | |
| `id` | string | _task identifier_
**unique task identifier in our system in the [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format** | |
| `status_code` | integer | _status code of the task_
generated by DataForSEO; can be within the following range: 10000-60000
you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) | |
| `status_message` | string | _informational message of the task_
you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix-errors/) | |
| `time` | string | _execution time, seconds_ | |
| `cost` | float | _cost of the task, USD_ | |
| `result_count` | integer | _number of elements in the `result` array_ | |
| `path` | array | _URL path_ | |
| `data` | object | _contains the same parameters that you specified in the POST request_ | |
| **`result`** | array | _array of results_ | |
| `se_type` | string | _search engine type_ | |
| `seed_keyword` | string | _keyword in a POST array_ | |
| **`seed_keyword_data`** | array | _keyword data for the seed keyword_
fields in the array are identical to that of `keyword_data` | |
| `location_code` | integer | _location code in a POST array_ | |
| `language_code` | string | _language code in a POST array_ | |
| `total_count` | integer | _total amount of results in our database relevant to your request_ | |
| `items_count` | integer | _the number of results returned in the `items` array_ | |
| `items` | array | _contains keywords and related data_ | |
| `se_type` | string | _search engine type_ | |
| `keyword_data` | object | _keyword data for the returned keyword_ | |
| `se_type` | string | _search engine type_ | |
| `keyword` | string | _related keyword_ | |
| `location_code` | integer | _location code in a POST array_ | |
| `language_code` | string | _language code in a POST array_ | |
| `keyword_info` | object | _keyword data for the returned keyword_ | |
| `se_type` | string | _search engine type_ | |
| `last_updated_time` | string | _date and time when keyword data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `competition` | float | _competition_
represents the relative amount of competition associated with the given keyword;
the value is based on Google Ads data and can be between 0 and 1 (inclusive) | |
| `competition_level` | string | _competition level_
represents the relative level of competition associated with the given keyword in paid SERP only;
possible values: `LOW`, `MEDIUM`, `HIGH`
if competition level is unknown, the value is `null`;
learn more about the metric in [this help center article](https://dataforseo.com/help-center/what-is-competition) | |
| `cpc` | float | _cost-per-click_
represents the average cost per click (USD) historically paid for the keyword | |
| `search_volume` | integer | _average monthly search volume rate_
represents the (approximate) number of searches for the given keyword idea on google.com | |
| `low_top_of_page_bid` | float | _minimum bid for the ad to be displayed at the top of the first page_
indicates the value greater than about 20% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)
the value may differ depending on the location specified in a POST request | |
| `high_top_of_page_bid` | float | _maximum bid for the ad to be displayed at the top of the first page_
indicates the value greater than about 80% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)
the value may differ depending on the location specified in a POST request | |
| `categories` | array | _product and service categories_
you can download the [full list of possible categories](https://cdn.dataforseo.com/v3/categories/categories_dataforseo_labs_2023_10_25.csv) | |
| `monthly_searches` | array | _monthly searches_
represents the (approximate) number of searches on this keyword idea (as available for the past twelve months), targeted to the specified geographic locations | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _monthly average search volume rate_ | |
| `search_volume_trend` | object | _search volume trend changes_
represents search volume change in percent compared to the previous period | |
| `monthly` | integer | _search volume change in percent compared to the previous month_ | |
| `quarterly` | integer | _search volume change in percent compared to the previous quarter_ | |
| `yearly` | integer | _search volume change in percent compared to the previous year_ | |
| `clickstream_keyword_info` | object | _clickstream data for the returned keyword_
to retrieve results for this field, the parameter `include_clickstream_data` must be set to `true` | |
| `search_volume` | integer | _monthly average clickstream search volume rate_ | |
| `last_updated_time` | string | _date and time when the clickstream dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” | |
| `gender_distribution` | object | _distribution of estimated clickstream-based metrics by gender_
learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `female` | integer | _number of female users in the relevant clickstream dataset_ | |
| `male` | integer | _number of male users in the relevant clickstream dataset_ | |
| `age_distribution` | object | _distribution of clickstream-based metrics by age_
learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) | |
| `18-24` | integer | _number of users in the relevant clickstream dataset that fall within the 18-24 age range_ | |
| `25-34` | integer | _number of users in the relevant clickstream dataset that fall within the 25-34 age range_ | |
| `35-44` | integer | _number of users in the relevant clickstream dataset that fall within the 35-44 age range_ | |
| `45-54` | integer | _number of users in the relevant clickstream dataset that fall within the 45-54 age range_ | |
| `55-64` | integer | _number of users in the relevant clickstream dataset that fall within the 55-64 age range_ | |
| `monthly_searches` | array | _monthly clickstream search volume rates_
array of objects with clickstream search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _clickstream-based search volume rate in a certain month of a year_ | |
| `keyword_properties` | object | _additional information about the keyword_ | |
| `se_type` | string | _search engine type_ | |
| `core_keyword` | string | _main keyword in a group_
contains the main keyword in a group determined by the synonym clustering algorithm
if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` | |
| `synonym_clustering_algorithm` | string | _the algorithm used to identify synonyms_
possible values:
`keyword_metrics` – indicates the algorithm based on `keyword_info` parameters
`text_processing` – indicates the text-based algorithm
if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` | |
| `keyword_difficulty` | integer | _difficulty of ranking in the first top-10 organic results for a keyword_
indicates the chance of getting in top-10 organic results for a keyword on a logarithmic scale from 0 to 100;
calculated by analysing, among other parameters, link profiles of the first 10 pages in SERP;
learn more about the metric in [this help center guide](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated) | |
| `detected_language` | string | _detected language of the keyword_
indicates the language of the keyword as identified by our system | |
| `is_another_language` | boolean | _detected language of the keyword is different from the set language_
if `true`, the language set in the request does not match the language determined by our system for a given keyword | |
| `serp_info` | object | _SERP data_
the value will be `null` if you didn’t set the field `include_serp_info` to `true` in the POST array or if there is no SERP data for this keyword in our database | |
| `se_type` | string | _search engine type_ | |
| `check_url` | string | _direct URL to search engine results_
you can use it to make sure that we provided accurate results | |
| `serp_item_types` | array | _types of search results in SERP_
contains types of search results (items) found in SERP
possible item types:
`answer_box`, `app`, `carousel`, `multi_carousel`, `featured_snippet`, `google_flights`, `google_reviews`, `third_party_reviews`, `google_posts`, `images`, `jobs`, `knowledge_graph`, `local_pack`, `hotels_pack`, `map`, `organic`, `paid`, `people_also_ask`, `related_searches`, `people_also_search`, `shopping`, `top_stories`, `twitter`, `video`, `events`, `mention_carousel`, `recipes`, `top_sights`, `scholarly_articles`, `popular_products`, `podcasts`, `questions_and_answers`, `find_results_on`, `stocks_box`, `visual_stories`, `commercial_units`, `local_services`, `google_hotels`, `math_solver`, `currency_box`, `product_considerations`, `found_on_web`, `short_videos`, `refine_products`, `explore_brands`, `perspectives`, `discussions_and_forums`, `compare_sites`, `courses`, `ai_overview`;
**note** that the actual results will be returned only for `organic`, `paid`, `featured_snippet`, and `local_pack` elements | |
| `se_results_count` | integer | _number of search results for the returned keyword_ | |
| `last_updated_time` | string | _date and time when SERP data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `previous_updated_time` | string | _previous to the most recent date and time when SERP data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-10-15 12:57:46 +00:00` | |
| `avg_backlinks_info` | object | _backlink data for the returned keyword_
this object provides the average number of backlinks, referring pages and domains, as well as the average rank values among the top-10 webpages ranking organically for the keyword | |
| `se_type` | string | _search engine type_ | |
| `backlinks` | float | _average number of backlinks_ | |
| `dofollow` | float | _average number of dofollow links_ | |
| `referring_pages` | float | _average number of referring pages_ | |
| `referring_domains` | float | _average number of referring domains_ | |
| `referring_main_domains` | float | _average number of referring main domains_ | |
| `rank` | float | _average rank_
learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) | |
| `main_domain_rank` | float | _average main domain rank_
learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) | |
| `last_updated_time` | string | _date and time when backlink data was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `search_intent_info` | object | _search intent info for the returned keyword_
learn about search intent in this [help center article](https://dataforseo.com/help-center/search-intent-and-its-types) | |
| `se_type` | string | _search engine type_
possible values: `google` | |
| `main_intent` | string | _main search intent_
possible values: `informational`, `navigational`, `commercial`, `transactional` | |
| `foreign_intent` | array | _supplementary search intents_
possible values: `informational`, `navigational`, `commercial`, `transactional` | |
| `last_updated_time` | string | _date and time when search intent data was last updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| **`keyword_info_normalized_with_bing`** | object | _contains keyword search volume normalized with Bing search volume_ | |
| `last_updated_time` | string | _date and time when the dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `search_volume` | integer | _current search volume rate of a keyword_ | |
| `is_normalized` | boolean | _keyword info is normalized_
if `true`, values are normalized with Bing data | |
| `monthly_searches` | integer | _monthly search volume rates_
array of objects with search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _search volume rate in a certain month of a year_ | |
| **`keyword_info_normalized_with_clickstream`** | object | _contains keyword search volume normalized with clickstream data_ | |
| `last_updated_time` | string | _date and time when the dataset was updated_
in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”
example:
`2019-11-15 12:57:46 +00:00` | |
| `search_volume` | integer | _current search volume rate of a keyword_ | |
| `is_normalized` | boolean | _keyword info is normalized_
if `true`, values are normalized with clickstream data | |
| `monthly_searches` | integer | _monthly search volume rates_
array of objects with search volume rates in a certain month of a year | |
| `year` | integer | _year_ | |
| `month` | integer | _month_ | |
| `search_volume` | integer | _search volume rate in a certain month of a year_ | |
| `depth` | integer | _keyword search depth_ | |
| `related_keywords` | array | _list of related keywords_
represents the list of search queries which are related to the keyword returned in the array above | |
SERP TYPES:
| `serp_item_types` | array | _types of search results in SERP_
contains types of search results (items) found in SERP
possible item types:
`answer_box`, `app`, `carousel`, `multi_carousel`, `featured_snippet`, `google_flights`, `google_reviews`, `third_party_reviews`, `google_posts`, `images`, `jobs`, `knowledge_graph`, `local_pack`, `hotels_pack`, `map`, `organic`, `paid`, `people_also_ask`, `related_searches`, `people_also_search`, `shopping`, `top_stories`, `twitter`, `video`, `events`, `mention_carousel`, `recipes`, `top_sights`, `scholarly_articles`, `popular_products`, `podcasts`, `questions_and_answers`, `find_results_on`, `stocks_box`, `visual_stories`, `commercial_units`, `local_services`, `google_hotels`, `math_solver`, `currency_box`, `product_considerations`, `found_on_web`, `short_videos`, `refine_products`, `explore_brands`, `perspectives`, `discussions_and_forums`, `compare_sites`, `courses`, `ai_overview`
FILTERES WE CNA USE:
"keyword_ideas": {
"google": {
"keyword": "str",
"keyword_info.last_updated_time": "time",
"keyword_info.competition": "num",
"keyword_info.competition_level": "str",
"keyword_info.cpc": "num",
"keyword_info.search_volume": "num",
"keyword_info.low_top_of_page_bid": "num",
"keyword_info.high_top_of_page_bid": "num",
"keyword_info.categories": "array.num",
"keyword_info.search_volume_trend.monthly": "num",
"keyword_info.search_volume_trend.quarterly": "num",
"keyword_info.search_volume_trend.yearly": "num",
"clickstream_keyword_info.search_volume": "num",
"clickstream_keyword_info.last_updated_time": "time",
"clickstream_keyword_info.gender_distribution.female": "num",
"clickstream_keyword_info.gender_distribution.male": "num",
"clickstream_keyword_info.age_distribution.18-24": "num",
"clickstream_keyword_info.age_distribution.25-34": "num",
"clickstream_keyword_info.age_distribution.35-44": "num",
"clickstream_keyword_info.age_distribution.45-54": "num",
"clickstream_keyword_info.age_distribution.55-64": "num",
"keyword_properties.core_keyword": "str",
"keyword_properties.synonym_clustering_algorithm": "str",
"keyword_properties.keyword_difficulty": "num",
"keyword_properties.detected_language": "str",
"keyword_properties.is_another_language": "bool",
"serp_info.check_url": "str",
"serp_info.serp_item_types": "array.str",
"serp_info.se_results_count": "num",
"serp_info.last_updated_time": "time",
"avg_backlinks_info.backlinks": "num",
"avg_backlinks_info.dofollow": "num",
"avg_backlinks_info.referring_pages": "num",
"avg_backlinks_info.referring_domains": "num",
"avg_backlinks_info.referring_main_domains": "num",
"avg_backlinks_info.rank": "num",
"avg_backlinks_info.main_domain_rank": "num",
"avg_backlinks_info.last_updated_time": "time",
"search_intent_info.main_intent": "str",
"search_intent_info.foreign_intent": "array.str",
"search_intent_info.last_updated_time": "time",
"keyword_info_normalized_with_bing.search_volume": "num",
"keyword_info_normalized_with_bing.last_updated_time": "time",
"keyword_info_normalized_with_bing.is_normalized": "bool",
"keyword_info_normalized_with_clickstream.search_volume": "num",
"keyword_info_normalized_with_clickstream.last_updated_time": "time",
"keyword_info_normalized_with_clickstream.is_normalized": "bool"
}
},
},
"keyword_suggestions": {
"google": {
"keyword": "str",
"keyword_info.last_updated_time": "time",
"keyword_info.competition": "num",
"keyword_info.competition_level": "str",
"keyword_info.cpc": "num",
"keyword_info.search_volume": "num",
"keyword_info.low_top_of_page_bid": "num",
"keyword_info.high_top_of_page_bid": "num",
"keyword_info.categories": "array.num",
"keyword_info.search_volume_trend.monthly": "num",
"keyword_info.search_volume_trend.quarterly": "num",
"keyword_info.search_volume_trend.yearly": "num",
"clickstream_keyword_info.search_volume": "num",
"clickstream_keyword_info.last_updated_time": "time",
"clickstream_keyword_info.gender_distribution.female": "num",
"clickstream_keyword_info.gender_distribution.male": "num",
"clickstream_keyword_info.age_distribution.18-24": "num",
"clickstream_keyword_info.age_distribution.25-34": "num",
"clickstream_keyword_info.age_distribution.35-44": "num",
"clickstream_keyword_info.age_distribution.45-54": "num",
"clickstream_keyword_info.age_distribution.55-64": "num",
"keyword_properties.core_keyword": "str",
"keyword_properties.synonym_clustering_algorithm": "str",
"keyword_properties.keyword_difficulty": "num",
"keyword_properties.detected_language": "str",
"keyword_properties.is_another_language": "bool",
"serp_info.check_url": "str",
"serp_info.se_results_count": "num",
"serp_info.last_updated_time": "time",
"serp_info.serp_item_types": "array.str",
"avg_backlinks_info.backlinks": "num",
"avg_backlinks_info.dofollow": "num",
"avg_backlinks_info.referring_pages": "num",
"avg_backlinks_info.referring_domains": "num",
"avg_backlinks_info.referring_main_domains": "num",
"avg_backlinks_info.rank": "num",
"avg_backlinks_info.main_domain_rank": "num",
"avg_backlinks_info.last_updated_time": "time",
"search_intent_info.main_intent": "str",
"search_intent_info.foreign_intent": "array.str",
"search_intent_info.last_updated_time": "time",
"keyword_info_normalized_with_bing.search_volume": "num",
"keyword_info_normalized_with_bing.last_updated_time": "time",
"keyword_info_normalized_with_bing.is_normalized": "bool",
"keyword_info_normalized_with_clickstream.search_volume": "num",
"keyword_info_normalized_with_clickstream.last_updated_time": "time",
"keyword_info_normalized_with_clickstream.is_normalized": "bool"
}
},
related_keywords": {
"google": {
"depth": "num",
"keyword_data.keyword": "str",
"keyword_data.keyword_info.last_updated_time": "time",
"keyword_data.keyword_info.competition": "num",
"keyword_data.keyword_info.competition_level": "str",
"keyword_data.keyword_info.cpc": "num",
"keyword_data.keyword_info.search_volume": "num",
"keyword_data.keyword_info.low_top_of_page_bid": "num",
"keyword_data.keyword_info.high_top_of_page_bid": "num",
"keyword_data.keyword_info.categories": "array.num",
"keyword_data.keyword_info.search_volume_trend.monthly": "num",
"keyword_data.keyword_info.search_volume_trend.quarterly": "num",
"keyword_data.keyword_info.search_volume_trend.yearly": "num",
"keyword_data.clickstream_keyword_info.search_volume": "num",
"keyword_data.clickstream_keyword_info.last_updated_time": "time",
"keyword_data.clickstream_keyword_info.gender_distribution.female": "num",
"keyword_data.clickstream_keyword_info.gender_distribution.male": "num",
"keyword_data.clickstream_keyword_info.age_distribution.18-24": "num",
"keyword_data.clickstream_keyword_info.age_distribution.25-34": "num",
"keyword_data.clickstream_keyword_info.age_distribution.35-44": "num",
"keyword_data.clickstream_keyword_info.age_distribution.45-54": "num",
"keyword_data.clickstream_keyword_info.age_distribution.55-64": "num",
"keyword_data.keyword_properties.core_keyword": "str",
"keyword_data.keyword_properties.synonym_clustering_algorithm": "str",
"keyword_data.keyword_properties.keyword_difficulty": "num",
"keyword_data.keyword_properties.detected_language": "str",
"keyword_data.keyword_properties.is_another_language": "bool",
"keyword_data.serp_info.check_url": "str",
"keyword_data.serp_info.serp_item_types": "array.str",
"keyword_data.serp_info.se_results_count": "num",
"keyword_data.serp_info.last_updated_time": "time",
"keyword_data.serp_info.previous_updated_time": "time",
"keyword_data.avg_backlinks_info.backlinks": "num",
"keyword_data.avg_backlinks_info.dofollow": "num",
"keyword_data.avg_backlinks_info.referring_pages": "num",
"keyword_data.avg_backlinks_info.referring_domains": "num",
"keyword_data.avg_backlinks_info.referring_main_domains": "num",
"keyword_data.avg_backlinks_info.rank": "num",
"keyword_data.avg_backlinks_info.main_domain_rank": "num",
"keyword_data.avg_backlinks_info.last_updated_time": "time",
"keyword_data.search_intent_info.main_intent": "str",
"keyword_data.search_intent_info.foreign_intent": "array.str",
"keyword_data.search_intent_info.last_updated_time": "time",
"keyword_data.keyword_info_normalized_with_bing.search_volume": "num",
"keyword_data.keyword_info_normalized_with_bing.last_updated_time": "time",
"keyword_data.keyword_info_normalized_with_bing.is_normalized": "bool",
"keyword_data.keyword_info_normalized_with_clickstream.search_volume": "num",
"keyword_data.keyword_info_normalized_with_clickstream.last_updated_time": "time",
"keyword_data.keyword_info_normalized_with_clickstream.is_normalized": "bool"
},



CODE:

This file is a merged representation of the entire codebase, combining all repository files into a single document.
Generated by Repomix on: 2025-11-04T09:34:44.279Z

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's
  configuration.
- Binary files are not included in this packed representation. Please refer to
  the Repository Structure section for a complete list of file paths, including
  binary files.

## Additional Info

# Directory Structure
```
keyword_discovery/
  expander.py
  filters.py
__init__.py
blog_content_qualifier.py
cannibalization_checker.py
disqualification_rules.py
keyword_expander.py
run_discovery.py
```

# Files

## File: keyword_discovery/expander.py
```python
# pipeline/step_01_discovery/keyword_discovery/expander.py
import logging
import json # NEW import for json.dumps
from typing import List, Dict, Any, Optional

from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from backend.data_mappers.dataforseo_mapper import DataForSEOMapper # NEW: Import for sanitization
from .filters import sanitize_filters_for_api # <--- 1. IMPORT THE FUNCTION


class NewKeywordExpander:
    def __init__(
        self,
        client: DataForSEOClientV2,
        config: Dict[str, Any],
        logger: Optional[logging.Logger] = None,
    ):
        self.client = client
        self.config = config
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def expand(
        self,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Dict[str, Any]]], # This is already the merged, goal-based filter list
        order_by: Optional[List[str]], # This is already the merged, goal-based order_by list
        existing_keywords: set,
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = False, # Legacy parameter, new overrides are preferred
        # NEW params for direct passthrough from DiscoveryRunRequest
        include_clickstream_data_override: Optional[bool] = None,
        closely_variants_override: Optional[bool] = None,
        exact_match_override: Optional[bool] = None,
    ) -> Dict[str, Any]:
        if not discovery_modes:
            raise ValueError("At least one discovery mode must be selected.")

        # Filter out seed keywords that already exist
        original_seed_count = len(seed_keywords)
        seed_keywords = [
            kw for kw in seed_keywords if kw.lower() not in existing_keywords
        ]
        if not seed_keywords:
            self.logger.info(
                "All seed keywords already exist in the database. Skipping expansion."
            )
            return {
                "total_cost": 0.0,
                "raw_counts": {},
                "total_raw_count": 0,
                "total_unique_count": 0,
                "final_keywords": [],
            }
        self.logger.info(
            f"Filtered seed keywords from {original_seed_count} to {len(seed_keywords)}."
        )

        location_code = self.config.get("location_code")
        language_code = self.config.get("language_code")
        if not location_code or not language_code:
            raise ValueError("Location and language codes must be set.")

        # Determine final parameter values, prioritizing overrides -> request -> client_cfg -> hardcoded default
        final_ignore_synonyms = ignore_synonyms if ignore_synonyms is not None else self.config.get("discovery_ignore_synonyms", False)
        final_include_clickstream_data = include_clickstream_data_override if include_clickstream_data_override is not None else self.config.get("include_clickstream_data", False)
        final_closely_variants = closely_variants_override if closely_variants_override is not None else self.config.get("closely_variants", False)
        final_exact_match = exact_match_override if exact_match_override is not None else self.config.get("discovery_exact_match", False)

        # --- Filter and Order_by Transformation Logic ---
        
        # 2. CALL THE SANITIZER FUNCTION HERE
        if filters:
            filters = sanitize_filters_for_api(filters)

        # The `filters` and `order_by` lists are now unified from goal presets.
        # The DataForSEOClientV2 will handle the transformation of the filters.
        structured_filters = {
            "Keyword Ideas": filters,
            "Keyword Suggestions": filters,
            "Related Keywords": filters,
        }

        ideas_suggestions_orderby_for_api = []
        related_orderby_for_api = []
        if order_by:
            for rule_str in order_by:
                parts = rule_str.split(',')
                field = parts[0]
                direction = parts[1]

                cleaned_field = field
                if field.startswith("keyword_data."):
                    cleaned_field = field[len("keyword_data."):]
                ideas_suggestions_orderby_for_api.append(f"{cleaned_field},{direction}")

                prefixed_field = field
                if not field.startswith("keyword_data."):
                    prefixed_field = f"keyword_data.{field}"
                related_orderby_for_api.append(f"{prefixed_field},{direction}")


        structured_orderby = {
            "Keyword Ideas": ideas_suggestions_orderby_for_api,
            "Keyword Suggestions": ideas_suggestions_orderby_for_api,
            "Related Keywords": related_orderby_for_api,
        }
        # --- END Filter and Order_by Transformation Logic ---


        # Make a single burst call to the DataForSEOClientV2
        all_ideas, total_cost = self.client.get_keyword_ideas(
            seed_keywords=seed_keywords,
            location_code=location_code,
            language_code=language_code,
            client_cfg=self.config,
            discovery_modes=discovery_modes,
            filters=structured_filters, # Use the structured filters
            order_by=structured_orderby, # Use the structured order_by
            limit=limit,
            depth=depth, # This depth is for Related Keywords API specifically
            ignore_synonyms_override=final_ignore_synonyms,
            include_clickstream_override=final_include_clickstream_data,
            closely_variants_override=final_closely_variants,
            exact_match_override=final_exact_match,
        )
        self.logger.info(
            f"Burst discovery completed. Found {len(all_ideas)} raw keyword ideas. Cost: ${total_cost:.4f}"
        )

        # Filter out any duplicates and existing keywords from the burst results
        final_keywords_deduplicated = []
        seen_keywords = set(
            existing_keywords
        )

        raw_counts = {"Keyword Ideas": 0, "Keyword Suggestions": 0, "Related Keywords": 0} # Corrected keys to match discovery_source from client_cfg list
        for item in all_ideas:
            kw_text = item.get("keyword", "").lower()
            if kw_text and kw_text not in seen_keywords:
                final_keywords_deduplicated.append(item)
                seen_keywords.add(kw_text)
                source = item.get("discovery_source")
                # Correctly map source names for counts based on how `discovery_source` is set in get_keyword_ideas
                if source == "keyword_ideas":
                    raw_counts["Keyword Ideas"] += 1
                elif source == "keyword_suggestions": # This includes 'keyword_suggestions_seed' too
                    raw_counts["Keyword Suggestions"] += 1
                elif source == "related":
                    raw_counts["Related Keywords"] += 1
            elif kw_text:
                self.logger.debug(
                    f"Skipping duplicate or existing keyword: {item.get('keyword')}"
                )

        self.logger.info(
            f"Total unique new keywords after deduplication: {len(final_keywords_deduplicated)}"
        )

        return {
            "total_cost": total_cost,
            "raw_counts": raw_counts,
            "total_raw_count": len(all_ideas),
            "total_unique_count": len(final_keywords_deduplicated),
            "final_keywords": final_keywords_deduplicated,
        }
```

## File: keyword_discovery/filters.py
```python
# pipeline/step_01_discovery/keyword_discovery/filters.py
import json
import logging
from typing import List, Any, Tuple, Dict

logger = logging.getLogger(__name__)

FORBIDDEN_API_FILTER_FIELDS = [
    "relevance",
    "sv_bing",
    "sv_clickstream",
]  # Define forbidden fields


def sanitize_filters_for_api(filters: List[Any]) -> List[Any]:
    """
    Removes any filters attempting to use forbidden internal metrics or data sources.
    """
    sanitized = []
    for item in filters:
        if isinstance(item, list) and len(item) >= 1 and isinstance(item[0], str):
            field_path = item[0].lower()
            if any(
                forbidden in field_path for forbidden in FORBIDDEN_API_FILTER_FIELDS
            ):
                logger.warning(
                    f"Forbidden field '{field_path}' detected in API filter. Removing it."
                )
                continue
        sanitized.append(item)
    return sanitized
```

## File: __init__.py
```python
# pipeline/step_01_discovery/__init__.py
```

## File: blog_content_qualifier.py
```python
# pipeline/step_01_discovery/blog_content_qualifier.py
from typing import Dict, Any, Tuple
from .disqualification_rules import apply_disqualification_rules


def assign_status_from_score(
    opportunity: Dict[str, Any], score: float, client_cfg: Dict[str, Any]
) -> Tuple[str, str]:
    """
    Assigns a final status to a keyword based on its score and hard disqualification rules.
    """
    # First, check for hard-stop, non-negotiable disqualification rules.
    is_disqualified, reason, is_hard_stop = apply_disqualification_rules(
        opportunity, client_cfg, cannibalization_checker=None
    )

    if is_disqualified and is_hard_stop:
        return "rejected", reason

    # If not hard-stopped, categorize based on the strategic score.
    if score >= client_cfg.get("qualified_threshold", 70):
        return "qualified", "Qualified: High strategic score."
    elif score >= client_cfg.get("review_threshold", 50):
        return "review", "Review: Moderate strategic score."
    else:
        return "rejected", f"Rejected: Low strategic score ({score:.1f})."
```

## File: cannibalization_checker.py
```python
import logging
from typing import List, Dict, Any
from urllib.parse import urlparse

from backend.data_access.database_manager import DatabaseManager


class CannibalizationChecker:
    def __init__(
        self,
        target_domain: str,
        dataforseo_client: Any,
        client_cfg: Dict[str, Any],
        db_manager: DatabaseManager,
    ):
        self.target_domain = (
            target_domain.lower().replace("www.", "") if target_domain else None
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.dataforseo_client = dataforseo_client
        self.client_cfg = client_cfg
        self.db_manager = db_manager

    def is_url_in_serp(
        self, serp_results: List[Dict[str, Any]], keyword: str, client_id: str
    ) -> bool:
        """
        Returns True if the target domain is found in the list of SERP results
        OR if the keyword already exists in the opportunities database for the client.
        """
        if self.db_manager.check_existing_keywords(client_id, [keyword]):
            self.logger.warning(
                f"Cannibalization detected: Keyword '{keyword}' already exists in the database for client '{client_id}'."
            )
            return True

        if not self.target_domain:
            return False

        for result in serp_results:
            try:
                url = result.get("url")
                if not url:
                    continue
                url_domain = urlparse(url).netloc.lower().replace("www.", "")
                if url_domain == self.target_domain or url_domain.endswith(
                    f".{self.target_domain}"
                ):
                    self.logger.warning(
                        f"Cannibalization detected: Found '{url}' in SERP for '{keyword}'."
                    )
                    return True
            except Exception:
                continue
        return False
```

## File: disqualification_rules.py
```python
# pipeline/step_01_discovery/disqualification_rules.py
import logging
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import numpy as np
from core import utils

from .cannibalization_checker import CannibalizationChecker


def apply_disqualification_rules(
    opportunity: Dict[str, Any],
    client_cfg: Dict[str, Any],
    cannibalization_checker: CannibalizationChecker,
) -> Tuple[bool, Optional[str], bool]:
    """
    Applies the comprehensive 20-rule set to disqualify a keyword based on data from the discovery phase.
    Reads all thresholds from client_cfg.
    Returns (is_disqualified, reason, is_hard_stop).
    """
    keyword = opportunity.get("keyword", "Unknown Keyword")

    # --- Failsafe Validation ---
    required_keys = [
        "keyword_info",
        "keyword_properties",
        "serp_info",
        "search_intent_info",
    ]
    for key in required_keys:
        if key not in opportunity or opportunity[key] is None:
            logging.getLogger(__name__).warning(
                f"Disqualifying '{keyword}' due to missing or null '{key}' data."
            )
            return True, f"Rule 1: Missing critical data structure ({key}).", True

    serp_info = opportunity.get("serp_info", {})
    if not serp_info:
        logging.getLogger(__name__).warning(
            f"Disqualifying '{keyword}' due to empty 'serp_info' data."
        )
        return True, "Rule 1: Missing SERP info data.", True

    keyword_info = opportunity.get("keyword_info") or {}
    keyword_props = opportunity.get("keyword_properties") or {}
    avg_backlinks = opportunity.get("avg_backlinks_info") or {}
    intent_info = opportunity.get("search_intent_info") or {}

    # New Rule: Reject if SV or KD data is missing (null)
    search_volume = keyword_info.get("search_volume")
    keyword_difficulty = keyword_props.get("keyword_difficulty")

    # A search volume of 0 is a valid reason to disqualify based on client strategy.
    if search_volume is None or search_volume == 0:
        return True, "Rule 0: Rejected due to zero or null Search Volume.", True
    
    # A keyword difficulty of 0 is a valid, desirable metric. Only reject if data is missing.
    if keyword_difficulty is None:
        return True, "Rule 0: Rejected due to null Keyword Difficulty.", True

    # Tier 1: Foundational Checks
    if not all([keyword_info, keyword_props, intent_info]):
        return (
            True,
            "Rule 1: Missing critical data structures (keyword_info, keyword_properties, or search_intent_info).",
            True,
        )

    # Rule 2: Check primary intent
    allowed_intents = client_cfg.get("allowed_intents", ["informational"])
    main_intent = intent_info.get("main_intent")
    foreign_intents = intent_info.get("foreign_intent", [])

    if main_intent not in allowed_intents:
        return True, f"Rule 2: Non-target main intent ('{main_intent}').", True

    # Rule 2b (NEW): Check secondary intents for prohibitive types
    prohibited_intents = set(client_cfg.get("prohibited_intents", ["navigational"]))
    foreign_intents = intent_info.get("foreign_intent", []) or []
    if not prohibited_intents.isdisjoint(set(foreign_intents)):
        offending_intents = prohibited_intents.intersection(set(foreign_intents))
        return (
            True,
            f"Rule 2b: Contains a prohibited secondary intent ({', '.join(offending_intents)}).",
            True,
        )

    if keyword_props.get("is_another_language"):
        return True, "Rule 3: Language mismatch.", True

    negative_keywords = set(
        kw.lower() for kw in client_cfg.get("negative_keywords", [])
    )
    core_keyword = keyword_props.get("core_keyword")
    if any(neg_kw in keyword.lower() for neg_kw in negative_keywords) or (
        core_keyword
        and any(neg_kw in core_keyword.lower() for neg_kw in negative_keywords)
    ):
        return True, "Rule 4: Contains a negative keyword.", True

    # Tier 2: Volume & Trend Analysis
    if utils.safe_compare(
        keyword_info.get("search_volume"), client_cfg.get("min_search_volume"), "lt"
    ):
        return (
            True,
            f"Rule 5: Below search volume floor (minimum: {client_cfg.get('min_search_volume', 100)} SV). Current: {keyword_info.get('search_volume', 0)} SV.",
            False,
        )

    trends = opportunity.get("keyword_info", {}).get("search_volume_trend", {})
    if trends:
        if not isinstance(trends, dict):
            logging.getLogger(__name__).warning(
                f"Skipping trend analysis for keyword '{keyword}' due to unexpected data type for trends: {type(trends)}"
            )
            return False, None, False
        try:
            yearly_trend = trends.get("yearly") if trends.get("yearly") is not None else 0
            quarterly_trend = trends.get("quarterly") if trends.get("quarterly") is not None else 0

            yearly_threshold = client_cfg.get("yearly_trend_decline_threshold", -25)
            quarterly_threshold = client_cfg.get("quarterly_trend_decline_threshold", 0)

            yearly_check = utils.safe_compare(yearly_trend, yearly_threshold, "lt")
            quarterly_check = utils.safe_compare(quarterly_trend, quarterly_threshold, "lt")

            if yearly_check and quarterly_check:
                return (
                    True,
                    f"Rule 6: Consistently declining trend. Yearly trend: {yearly_trend}% (below {yearly_threshold}% threshold), Quarterly trend: {quarterly_trend}% (below {quarterly_threshold}% threshold). Consider manual review for seasonality.",
                    False,
                )
        except TypeError:
            logging.getLogger(__name__).error(
                f"TypeError during trend analysis for keyword '{keyword}'. "
                f"trends.get('yearly') value: {trends.get('yearly')}, type: {type(trends.get('yearly'))}. "
                f"trends.get('quarterly') value: {trends.get('quarterly')}, type: {type(trends.get('quarterly'))}."
            )
            return (
                True,
                "Rule 6: Failed to process trend data due to invalid format.",
                False,
            )

    monthly_searches = keyword_info.get("monthly_searches", [])
    if monthly_searches and len(monthly_searches) > 1:
        volumes = [
            ms["search_volume"]
            for ms in monthly_searches
            if ms.get("search_volume") is not None and ms["search_volume"] > 0
        ]
        if len(volumes) > 1 and np.mean(volumes) > 0:
            volatility_threshold = client_cfg.get(
                "search_volume_volatility_threshold", 1.5
            )
            std_dev_to_mean_ratio = np.std(volumes) / np.mean(volumes)
            if std_dev_to_mean_ratio > volatility_threshold:
                return (
                    True,
                    f"Rule 7: Extreme search volume volatility. Std Dev / Mean ratio: {std_dev_to_mean_ratio:.2f} (above {volatility_threshold} threshold). Could indicate a fleeting trend or strong seasonality. Manual review recommended.",
                    False,
                )

    # Rule 7b: Check for recent sharp decline using raw monthly searches
    monthly_searches = opportunity.get(
        "monthly_searches", []
    )  # Get from opportunity object, which is deserialized
    if monthly_searches and len(monthly_searches) >= 4:
        # Sort by year and month to ensure correctness (most recent first for trend)
        try:
            sorted_searches = sorted(
                monthly_searches, key=lambda x: (x["year"], x["month"]), reverse=True
            )
            if len(sorted_searches) >= 4:
                # Compare latest month with 3 months prior (index 0 vs index 3)
                latest_vol = sorted_searches[0].get("search_volume")
                past_vol = sorted_searches[3].get("search_volume")

                if latest_vol is not None and past_vol is not None and past_vol > 0:
                    if (
                        latest_vol / past_vol
                    ) < 0.5:  # If volume has dropped by more than 50% in 3 months
                        return (
                            True,
                            "Rule 7b: Recent sharp decline in search volume (>50% drop in last 3 months).",
                            False,
                        )
        except (TypeError, KeyError):
            logging.getLogger(__name__).warning(
                f"Could not parse monthly_searches for recent trend analysis on keyword '{keyword}'."
            )

    # Tier 3: Commercial & Competitive Analysis
    if utils.safe_compare(
        keyword_info.get("competition"),
        client_cfg.get("max_paid_competition_score", 0.8),
        "gt",
    ) and (keyword_info.get("competition_level") == "HIGH"):
        return True, "Rule 8: Excessive paid competition.", False

    if utils.safe_compare(
        keyword_info.get("high_top_of_page_bid"),
        client_cfg.get("max_high_top_of_page_bid", 15.0),
        "gt",
    ):
        return (
            True,
            f"Rule 9: Prohibitively high CPC bids (${client_cfg.get('max_high_top_of_page_bid', 15.00)}).",
            False,
        )

    if utils.safe_compare(
        keyword_props.get("keyword_difficulty"),
        client_cfg.get("max_kd_hard_limit", 70),
        "gt",
    ):
        return (
            True,
            f"Rule 10: Extreme keyword difficulty (>{client_cfg.get('max_kd_hard_limit', 70)}).",
            False,
        )

    if utils.safe_compare(
        avg_backlinks.get("referring_main_domains"),
        client_cfg.get("max_referring_main_domains_limit", 100),
        "gt",
    ):
        return (
            True,
            f"Rule 11: Overly authoritative competitor domains (>{client_cfg.get('max_referring_main_domains_limit', 100)} referring main domains).",
            False,
        )

    if utils.safe_compare(
        avg_backlinks.get("main_domain_rank"),
        client_cfg.get("max_avg_domain_rank_threshold", 500),
        "lt",
    ):
        return (
            True,
            f"Rule 12: SERP dominated by high-authority domains (avg rank < {client_cfg.get('max_avg_domain_rank_threshold', 500)}).",
            False,
        )

    if (avg_backlinks.get("referring_domains") or 0) > 0:
        pages_to_domain_ratio = (avg_backlinks.get("referring_pages") or 0) / (
            avg_backlinks.get("referring_domains") or 1
        )
        if pages_to_domain_ratio > client_cfg.get("max_pages_to_domain_ratio", 15):
            return (
                True,
                "Rule 13: Potential spammy competitor profile (high page/domain ratio).",
                False,
            )

    # Tier 4: Content, SERP & Keyword Structure

    # Rule: Check for hostile SERP environment
    is_hostile, hostile_reason = _check_hostile_serp_environment(opportunity)
    if is_hostile:
        return True, hostile_reason, True

    non_evergreen_pattern = _get_non_evergreen_year_pattern()
    if non_evergreen_pattern and re.search(non_evergreen_pattern, keyword):
        return (
            True,
            "Rule 14: Non-evergreen temporal keyword (matches pattern for past/current years).",
            False,
        )

    word_count = len(keyword.split())
    is_question = utils.is_question_keyword(keyword)  # This now exists

    min_wc = client_cfg.get("min_keyword_word_count", 2)
    max_wc = client_cfg.get("max_keyword_word_count", 8)

    is_outside_range = word_count < min_wc or word_count > max_wc

    # Rule 15 (Refined with override): Check word count and potentially override for high-value keywords
    if is_outside_range and not is_question:
        sv = keyword_info.get("search_volume", 0)
        cpc = keyword_info.get("cpc")  # Get the value, which could be None
        if cpc is None:
            cpc = 0.0  # Default to 0.0 if it's None

        high_sv_override = client_cfg.get("high_value_sv_override_threshold", 10000)
        high_cpc_override = client_cfg.get("high_value_cpc_override_threshold", 5.0)

        if sv >= high_sv_override or cpc >= high_cpc_override:
            logging.getLogger(__name__).info(
                f"Override: High value SV/CPC bypasses word count rule for '{keyword}'."
            )
            pass  # Allow the keyword to proceed
        else:
            return (
                True,
                f"Rule 15: Non-question keyword word count ({word_count}) is outside the acceptable range ({min_wc}-{max_wc} words).",
                False,
            )

    serp_info = opportunity.get("serp_info", {})
    serp_types = set(serp_info.get("serp_item_types", []))

    crowded_features = {
        "video",
        "images",
        "people_also_ask",
        "carousel",
        "featured_snippet",
        "short_videos",
    }
    if len(serp_types.intersection(crowded_features)) > client_cfg.get(
        "crowded_serp_features_threshold", 4
    ):
        return (
            True,
            f"Rule 17: SERP is overly crowded (>{client_cfg.get('crowded_serp_features_threshold', 4)} attention-grabbing features).",
            False,
        )

    # Rule 18: Check for navigational intent safely
    is_navigational = False
    if intent_info:
        if intent_info.get("main_intent") == "navigational":
            is_navigational = True
        else:
            foreign_intent = intent_info.get("foreign_intent")
            if foreign_intent and "navigational" in foreign_intent:
                is_navigational = True
    if is_navigational:
        return True, "Rule 18: Strong navigational intent.", True

    if serp_info.get("last_updated_time") and serp_info.get("previous_updated_time"):
        try:
            last_update = datetime.fromisoformat(
                serp_info["last_updated_time"].replace(" +00:00", "")
            )
            prev_update = datetime.fromisoformat(
                serp_info["previous_updated_time"].replace(" +00:00", "")
            )
            days_between_updates = (last_update - prev_update).days
            if days_between_updates < client_cfg.get("min_serp_stability_days", 14):
                return (
                    True,
                    f"Rule 19: Unstable SERP (updated every {days_between_updates} days).",
                    False,
                )
        except ValueError:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP update times for '{keyword}': {serp_info.get('last_updated_time')}, {serp_info.get('previous_updated_time')}"
            )

    cpc_value = keyword_info.get("cpc")
    if cpc_value is None:
        cpc_value = 0.0
    if (
        intent_info.get("main_intent") in ["commercial", "transactional"]
        and cpc_value == 0
    ):
        return True, "Rule 20: Low-value commercial intent (zero CPC).", False

    return False, None, False


def _check_hostile_serp_environment(
    opportunity: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    """
    Rule 16: Disqualifies keywords where the SERP is dominated by features hostile to blog content.
    """
    serp_info = opportunity.get("serp_info", {})
    if not serp_info:
        return False, None  # Cannot analyze if SERP info is missing

    serp_types = set(serp_info.get("serp_item_types", []))

    # Define hostile features based on detailed SERP analysis
    HOSTILE_FEATURES = {
        # Strong transactional/e-commerce intent
        "shopping",
        "popular_products",
        "refine_products",
        "explore_brands",
        # Strong local intent
        "local_pack",
        "map",
        "local_services",
        # Purely transactional/utility intent (Google-owned tools)
        "google_flights",
        "google_hotels",
        "hotels_pack",
        # App-related intent
        "app",
        # Job-seeking intent
        "jobs",
        # Direct utility/tool intent
        "math_solver",
        "currency_box",
        "stocks_box",
    }

    found_hostile_features = serp_types.intersection(HOSTILE_FEATURES)

    if found_hostile_features:
        return (
            True,
            f"Rule 16: SERP is hostile to blog content. Contains dominant non-article features: {', '.join(found_hostile_features)}.",
        )

    return False, None


def _get_non_evergreen_year_pattern() -> str:
    """
    Generates a regex pattern to find past years up to the current year,
    dynamically adjusting to avoid disqualifying valid keywords in the future.
    Example for current year 2024: \b(201\d|202[0-4])\b
    """
    current_year = datetime.now().year

    patterns = []
    # Handle decades before the current one (e.g., 2010s)
    for decade_start in range(2010, (current_year // 10) * 10, 10):
        patterns.append(
            f"{decade_start}|{decade_start + 1}|{decade_start + 2}|{decade_start + 3}|{decade_start + 4}|{decade_start + 5}|{decade_start + 6}|{decade_start + 7}|{decade_start + 8}|{decade_start + 9}"
        )

    # Handle years in the current decade up to the current year
    current_decade_start_year = (current_year // 10) * 10
    current_decade_years = [
        str(year) for year in range(current_decade_start_year, current_year + 1)
    ]
    if current_decade_years:
        patterns.append("|".join(current_decade_years))

    if not patterns:
        return ""  # Should not happen unless current_year is before 2010

    return r"\b(" + "|".join(patterns) + r")\b"
```

## File: keyword_expander.py
```python
# pipeline/step_01_discovery/keyword_expander.py
import logging
from typing import List, Dict, Any, Optional
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from .keyword_discovery.expander import NewKeywordExpander


class KeywordExpander:
    """
    A wrapper class that uses the new modular keyword expansion system.
    """

    def __init__(
        self,
        client: DataForSEOClientV2,
        config: Dict[str, Any],
        run_logger: Optional[logging.Logger] = None,
    ):
        self.client = client
        self.config = config
        self.logger = run_logger or logging.getLogger(self.__class__.__name__)
        self.expander = NewKeywordExpander(client, config, self.logger)

    def expand_seed_keyword(
        self,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Dict[str, Any]]], # The merged list from router
        order_by: Optional[List[str]],
        existing_keywords: set,
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = False, # Legacy parameter, new overrides are preferred
        # NEW params for direct passthrough from DiscoveryRunRequest
        include_clickstream_data: Optional[bool] = None,
        closely_variants: Optional[bool] = None,
        exact_match: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Delegates the keyword expansion to the new NewKeywordExpander.
        """
        self.logger.info(
            f"Starting keyword expansion with {len(seed_keywords)} seeds and modes: {discovery_modes}"
        )

        results = self.expander.expand(
            seed_keywords,
            discovery_modes,
            filters, # Pass the merged filters here
            order_by,
            existing_keywords,
            limit,
            depth,
            ignore_synonyms,
            # NEW params
            include_clickstream_data,
            closely_variants,
            exact_match,
        )

        self.logger.info(
            f"Keyword expansion complete. Found {results['total_unique_count']} unique keywords."
        )

        return results
```

## File: run_discovery.py
```python
import logging
from typing import List, Dict, Any, Optional

from data_access.database_manager import DatabaseManager
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from pipeline.step_01_discovery.keyword_expander import KeywordExpander
from pipeline.step_01_discovery.disqualification_rules import (
    apply_disqualification_rules,
)
from pipeline.step_01_discovery.cannibalization_checker import CannibalizationChecker
from pipeline.step_03_prioritization.scoring_engine import ScoringEngine
from pipeline.step_01_discovery.blog_content_qualifier import assign_status_from_score



def run_discovery_phase(
    seed_keywords: List[str],
    dataforseo_client: DataForSEOClientV2,
    db_manager: "DatabaseManager",
    client_id: str,
    client_cfg: Dict[str, Any],
    discovery_modes: List[str],
    filters: Optional[List[Dict[str, Any]]], # It now receives the merged list of filters
    order_by: Optional[List[str]],
    limit: Optional[int] = None,
    depth: Optional[int] = None,
    ignore_synonyms: Optional[bool] = False,
    # NEW params for direct passthrough
    include_clickstream_data: Optional[bool] = None,
    closely_variants: Optional[bool] = None,
    exact_match: Optional[bool] = None,
    run_logger: Optional[logging.Logger] = None,
) -> Dict[str, Any]:
    logger = run_logger or logging.getLogger(__name__)
    logger.info("--- Starting Consolidated Keyword Discovery & Scoring Phase ---")

    expander = KeywordExpander(dataforseo_client, client_cfg, logger)
    cannibalization_checker = CannibalizationChecker(
        client_cfg.get("target_domain"), dataforseo_client, client_cfg, db_manager
    )
    scoring_engine = ScoringEngine(client_cfg)

    # 1. Get keywords that already exist for this client to avoid API calls for them.
    existing_keywords = set(db_manager.get_all_processed_keywords_for_client(client_id))
    logger.info(
        f"Found {len(existing_keywords)} existing keywords to exclude from API request."
    )

    # 2. Expand seed keywords into a large list of opportunities.
    expansion_result = expander.expand_seed_keyword(
        seed_keywords,
        discovery_modes,
        filters, # Pass the merged filters here
        order_by,
        existing_keywords,
        limit,
        depth,
        ignore_synonyms,
        # NEW params
        include_clickstream_data,
        closely_variants,
        exact_match,
    )

    all_expanded_keywords = expansion_result.get("final_keywords", [])
    total_cost = expansion_result.get("total_cost", 0.0)

    # --- Scoring and Disqualification Loop (Consolidated Logic) ---
    processed_opportunities = []
    disqualification_reasons = {}
    status_counts = {"qualified": 0, "review": 0, "rejected": 0}
    required_keys = [
        "keyword_info",
        "keyword_properties",
        "serp_info",
        "search_intent_info",
    ]

    for opp in all_expanded_keywords:
        # Pre-validation of opportunity structure
        missing_keys = [
            key for key in required_keys if key not in opp or opp[key] is None
        ]
        if missing_keys:
            logger.warning(
                f"Skipping opportunity '{opp.get('keyword')}' due to missing required data: {', '.join(missing_keys)}"
            )
            continue

        # 3. Apply Hard Disqualification Rules (Cannibalization, Negative Keywords, etc.)
        is_disqualified, reason, is_hard_stop = apply_disqualification_rules(
            opp, client_cfg, cannibalization_checker
        )

        if is_disqualified and is_hard_stop:
            opp["status"] = "rejected"
            opp["blog_qualification_status"] = "rejected"
            opp["blog_qualification_reason"] = reason
            status_counts["rejected"] += 1
            disqualification_reasons[reason] = (
                disqualification_reasons.get(reason, 0) + 1
            )
        else:
            # 4. Score the remaining keywords
            score, breakdown = scoring_engine.calculate_score(opp)
            opp["strategic_score"] = score
            opp["score_breakdown"] = breakdown

            # 5. Assign Status based on Strategic Score
            status, reason = assign_status_from_score(opp, score, client_cfg)
            opp["status"] = status
            opp["blog_qualification_status"] = status
            opp["blog_qualification_reason"] = reason
            status_counts[status.split("_")[0]] = (
                status_counts.get(status.split("_")[0], 0) + 1
            )  # count qualified/review/rejected

        processed_opportunities.append(opp)

    disqualified_count = status_counts.get("rejected", 0)
    passed_count = status_counts.get("qualified", 0) + status_counts.get("review", 0)

    logger.info(
        f"Scoring and Qualification complete. Passed: {passed_count}, Rejected: {disqualified_count}."
    )

    stats = {
        **expansion_result,
        "disqualification_reasons": disqualification_reasons,
        "disqualified_count": disqualified_count,
        "final_qualified_count": passed_count,
    }

    return {
        "stats": stats,
        "total_cost": total_cost,
        "opportunities": processed_opportunities,
    }
```
