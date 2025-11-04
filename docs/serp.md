
## Live Google Organic SERP Advanced

‌

### **Note:** the default value for the `depth` parameter has been updated from 100 to 10. Corresponding pricing changes are already in effect. [Full details >>](https://dataforseo.com/update/organic-serp-api-pricing-changes-now-in-effect)

Live SERP provides real-time data on top search engine results for the specified keyword, search engine, and location. This endpoint will supply a complete overview of featured snippets and other extra elements of SERPs.

> Instead of ‘login’ and ‘password’ use your credentials from https://app.dataforseo.com/api-access

```

Plain text

Copy to clipboard

Open code in new window

EnlighterJS 3 Syntax Highlighter

# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access \

login="login"

password="password"

cred="$(printf ${login}:${password} | base64)"

curl --location --request POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \

--header "Authorization: Basic ${cred}"  \

--header "Content-Type: application/json" \

--data-raw '[\
\
  {\
\
      "language_code": "en",\
\
      "location_code": 2840,\
\
      "keyword": "albert einstein",\
\
      "calculate_rectangles": true\
\
  }\
\
]'
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access \
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"
curl --location --request POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
--header "Authorization: Basic ${cred}"  \
--header "Content-Type: application/json" \
--data-raw '[\
  {\
      "language_code": "en",\
      "location_code": 2840,\
      "keyword": "albert einstein",\
      "calculate_rectangles": true\
  }\
]'
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access \
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"
curl --location --request POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
--header "Authorization: Basic ${cred}"  \
--header "Content-Type: application/json" \
--data-raw '[\
  {\
      "language_code": "en",\
      "location_code": 2840,\
      "keyword": "albert einstein",\
      "calculate_rectangles": true\
  }\
]'

```

```
All POST data should be sent in the [JSON](https://en.wikipedia.org/wiki/JSON) format (UTF-8 encoding). When setting a task, you should send all task parameters in the task array of the generic POST array. You can send up to 2000 API calls per minute, each Live SERP API call can contain only one task.\
\
Below you will find a detailed description of the fields you can use for setting a task.\
\
**Description of the fields for setting a task:**\
\
| Field name | Type | Description |\
| --- | --- | --- |\
| `keyword` | string | _keyword_<br>**required field**<br>you can specify **up to 700 characters** in the `keyword` field<br>all %## will be decoded (plus character ‘+’ will be decoded to a space character)<br>if you need to use the “%” character for your `keyword`, please specify it as “%25”;<br>if you need to use the “+” character for your `keyword`, please specify it as “%2B”;<br>if this field contains such parameters as _‘allinanchor:’, ‘allintext:’, ‘allintitle:’, ‘allinurl:’, ‘define:’, ‘definition:’, ‘filetype:’, ‘id:’, ‘inanchor:’, ‘info:’, ‘intext:’, ‘intitle:’, ‘inurl:’, ‘link:’, ‘site:’_, **the charge per task will be multiplied by 5**<br>**Note:** queries containing the ‘cache:’ parameter are not supported and will return a validation error<br>learn more about rules and limitations of `keyword` and `keywords` fields in DataForSEO APIs in this [Help Center article](https://dataforseo.com/help-center/rules-and-limitations-of-keyword-and-keywords-fields-in-dataforseo-apis) |  |\
| `url` | string | _direct URL of the search query_<br>optional field<br>you can specify a direct URL and we will sort it out to the necessary fields. Note that this method is the most difficult for our API to process and also requires you to specify the exact language and location in the URL. In most cases, we wouldn’t recommend using this method.<br>example:<br>`https://www.google.co.uk/search?q=%20rank%20tracker%20api&hl=en&gl=GB&uule=w+CAIQIFISCXXeIa8LoNhHEZkq1d1aOpZS` |  |\
| `depth` | integer | _parsing depth_<br>optional field<br>number of results in SERP<br>**default value: `10`**<br>max value: `700`<br>**Note:** your account will be billed per each SERP containing up to 10 results;<br>thus, setting a depth above `10` may result in additional charges if the search engine returns more than 10 results;<br>if the specified depth is higher than the number of results in the response, the difference will be refunded automatically to your account balance |  |\
| `max_crawl_pages` | integer | _page crawl limit_<br>optional field<br>number of search results pages to crawl<br>max value: `100`<br>**Note:** you will be charged for each page crawled (10 organic results per page);<br>learn more about pricing on our [Pricing](https://dataforseo.com/pricing/serp/google-organic-serp-api) page;<br>**Note#2:** the `max_crawl_pages` and `depth` parameters complement each other;<br>learn more at [our help center](https://dataforseo.com/help-center/what-is-max-crawl-pages-and-how-does-it-work) |  |\
| `location_name` | string | _full name of search engine location_<br>**required field if you don’t specify** `location_code` or `location_coordinate`<br>**if you use this field, you don’t need to specify `location_code` or `location_coordinate`**<br>you can receive the list of available locations of the search engine with their `location_name` by making a separate request to the `https://api.dataforseo.com/v3/serp/google/locations`<br>example:<br>`London,England,United Kingdom` |  |\
| `location_code` | integer | _search engine location code_<br>**required field if you don’t specify** `location_name` or `location_coordinate`<br>**if you use this field, you don’t need to specify `location_name` or `location_coordinate`**<br>you can receive the list of available locations of the search engines with their `location_code` by making a separate request to the `https://api.dataforseo.com/v3/serp/google/locations`<br>example:<br>`2840` |  |\
| `location_coordinate` | string | _GPS coordinates of a location_<br>optional field if you specify `location_name` or `location_code`<br>**if you use this field, you don’t need to specify `location_name` or `location_code`**<br>`location_coordinate` parameter should be specified in the _“latitude,longitude,radius”_ format<br>the maximum number of decimal digits for _“latitude”_ and _“longitude”_: 7<br>the minimum value for _“radius”_: 199.9 (mm)<br>the maximum value for _“radius”_: 199999 (mm)<br>example:<br>`53.476225,-2.243572,200` |  |\
| `language_name` | string | _full name of search engine language_<br>optional field if you specify `language_code`<br>**if you use this field, you don’t need to specify `language_code`**<br>you can receive the list of available languages of the search engine with their `language_name` by making a separate request to the `https://api.dataforseo.com/v3/serp/google/languages`<br>example:<br>`English` |  |\
| `language_code` | string | _search engine language code_<br>optional field if you specify `language_name`<br>**if you use this field, you don’t need to specify `language_name`**<br>you can receive the list of available languages of the search engine with their `language_code` by making a separate request to the `https://api.dataforseo.com/v3/serp/google/languages` example: `en` |  |\
| `se_domain` | string | _search engine domain_<br>optional field<br>we choose the relevant search engine domain automatically according to the location and language you specify<br>however, you can set a custom search engine domain in this field<br>example:<br>_google.co.uk_, `google.com.au`, `google.de`, etc. |  |\
| `device` | string | _device type_<br>optional field<br>can take the values: `desktop`, `mobile`<br>default value: `desktop` |  |\
| `os` | string | _device operating system_<br>optional field<br>if you specify `desktop` in the `device` field, choose from the following values: `windows`, `macos`<br>default value: `windows`<br>if you specify `mobile` in the `device` field, choose from the following values: `android`, `ios`<br>default value: `android` |  |\
| `target` | string | _target domain, subdomain, or webpage to get results for_<br>optional field<br>a domain or a subdomain should be specified without `https://` and `www.`<br>note that the results of `target`-specific tasks will only include SERP elements that contain a `url` string;<br>you can also use a wildcard (‘\*’) character to specify the search pattern in SERP and narrow down the results;<br>examples:<br>**`example.com`** – returns results for the website’s home page with URLs, such as `https://example.com`, or `https://www.example.com/`, or `https://example.com/`;<br>**`example.com*`** – returns results for the domain, including all its pages;<br>**`*example.com*`** – returns results for the entire domain, including all its pages and subdomains;<br>**`*example.com`** – returns results for the home page regardless of the subdomain, such as `https://en.example.com`;<br>**`example.com/example-page`** – returns results for the exact URL;<br>**`example.com/example-page*`** – returns results for all domain’s URLs that start with the specified string |  |\
| `group_organic_results` | boolean | _display related results_<br>optional field<br>if set to `true`, the `related_result` element in the response will be provided as a snippet of its parent organic result;<br>if set to `false`, the `related_result` element will be provided as a separate organic result;<br>default value: `true` |  |\
| `calculate_rectangles` | boolean | _calcualte pixel rankings for SERP elements in advanced results_<br>optional field<br>pixel ranking refers to the distance between the result snippet and top left corner of the screen;<br>[Visit Help Center to learn more>>](https://dataforseo.com/help-center/pixel-ranking-in-serp-api)<br>by default, the parameter is set to `false`;<br>**Note:** you will be charged extra $0.002 for using this parameter |  |\
| `browser_screen_width` | integer | _browser screen width_<br>optional field<br>you can set a custom browser screen width to calculate pixel rankings for a particular device;<br>by default, the parameter is set to:<br>`1920` for `desktop`;<br>`360` for `mobile` on `android`;<br>`375` for `mobile` on `iOS`;<br>**Note:** to use this parameter, set `calculate_rectangles` to `true` |  |\
| `browser_screen_height` | integer | _browser screen height_<br>optional field<br>you can set a custom browser screen height to calculate pixel rankings for a particular device;<br>by default, the parameter is set to:<br>`1080` for `desktop`;<br>`640` for `mobile` on `android`;<br>`812` for `mobile` on `iOS`;<br>**Note:** to use this parameter, set `calculate_rectangles` to `true` |  |\
| `browser_screen_resolution_ratio` | integer | _browser screen resolution ratio_<br>optional field<br>you can set a custom browser screen resolution ratio to calculate pixel rankings for a particular device;<br>possible values: from `1` to `3`;<br>by default, the parameter is set to:<br>`1` for `desktop`;<br>`3` for `mobile` on `android`;<br>`3` for `mobile` on `iOS`;<br>**Note:** to use this parameter, set `calculate_rectangles` to `true` |  |\
| `people_also_ask_click_depth` | integer | _clicks on the corresponding element_<br>optional field<br>specify the click depth on the `people_also_ask` element to get additional `people_also_ask_element` items;<br>**Note** your account will be billed $0.00015 extra for each click;<br>if the element is absent or we perform fewer clicks than you specified, all extra charges will be returned to your account balance<br>possible values: from `1` to `4` |  |\
| `load_async_ai_overview` | boolean | _load asynchronous ai overview_<br>optional field<br>set to `true` to obtain `ai_overview` items is SERPs even if they are loaded asynchronically;<br>if set to `false`, you will only obtain `ai_overview` items from cache;<br>default value: `false`<br>**Note:** you will be charged extra $0.002 for using this parameter;<br>if the element is absent or contains `"asynchronous_ai_overview": false`, all extra charges will be returned to your account balance |  |\
| `search_param` | string | _additional parameters of the search query_<br>optional field<br>[get the list of available parameters and additional details here](https://dataforseo.com/help-center/google-search-engine-parameters-and-how-to-use-them) |  |\
| `remove_from_url` | array | _remove specific parameters from URLs_<br>optional field<br>using this field, you can specify up to 10 parameters to remove from URLs in the result<br>example:<br>`"remove_from_url": ["srsltid"]`<br>**Note:** if the `target` field is specified, the specified URL parameters will be removed before the search |  |\
| `tag` | string | _user-defined task identifier_<br>optional field<br>_the character limit is 255_<br>you can use this parameter to identify the task and match it with the result<br>you will find the specified `tag` value in the `data` object of the response |  |\
\
‌‌‌\
\
As a response of the API server, you will receive [JSON](https://en.wikipedia.org/wiki/JSON)-encoded data containing a `tasks` array with the information specific to the set tasks.\
\
**Description of the fields in the results array:**\
\
| Field name | Type | Description |\
| --- | --- | --- |\
| `version` | string | _the current version of the API_ |  |\
| `status_code` | integer | _general status code_<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors)<br>**Note:** we strongly recommend designing a necessary system for handling related exceptional or error conditions |  |\
| `status_message` | string | _general informational message_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) |  |\
| `time` | string | _execution time, seconds_ |  |\
| `cost` | float | _total tasks cost, USD_ |  |\
| `tasks_count` | integer | _the number of tasks in the **`tasks`** array_ |  |\
| `tasks_error` | integer | _the number of tasks in the **`tasks`** array returned with an error_ |  |\
| **`tasks`** | array | _array of tasks_ |  |\
| `id` | string | _task identifier_<br>**unique task identifier in our system in the [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format** |  |\
| `status_code` | integer | _status code of the task_<br>generated by DataForSEO; can be within the following range: 10000-60000<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) |  |\
| `status_message` | string | _informational message of the task_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) |  |\
| `time` | string | _execution time, seconds_ |  |\
| `cost` | float | _cost of the task, USD_ |  |\
| `result_count` | integer | _number of elements in the `result` array_ |  |\
| `path` | array | _URL path_ |  |\
| `data` | object | _contains the same parameters that you specified in the POST request_ |  |\
| **`result`** | array | _array of results_ |  |\
| `keyword` | string | _keyword received in a POST array_ **the keyword is returned with decoded %## (plus character ‘+’ will be decoded to a space character)** |  |\
| `type` | string | _search engine type in a POST array_ |  |\
| `se_domain` | string | _search engine domain in a POST array_ |  |\
| `location_code` | integer | _location code in a POST array_ |  |\
| `language_code` | string | _language code in a POST array_ |  |\
| `check_url` | string | _direct URL to search engine results_<br>you can use it to make sure that we provided accurate results |  |\
| `datetime` | string | _date and time when the result was received_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `spell` | object | _autocorrection of the search engine_<br>if the search engine provided results for a keyword that was corrected, we will specify the keyword corrected by the search engine and the type of autocorrection |  |\
| `keyword` | string | _keyword obtained as a result of search engine autocorrection_<br>the results will be provided for the corrected keyword |  |\
| `type` | string | _type of autocorrection_<br>possible values:<br>`did_you_mean`, `showing_results_for`, `no_results_found_for`, `including_results_for` |  |\
| `refinement_chips` | object | _search refinement chips_ |  |\
| `type` | string | _type of element = **‘refinement\_chips’**_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _items of the element_ |  |\
| `type` | string | _type of element = **‘refinement\_chips\_element’**_ |  |\
| `title` | string | _title of the element_ |  |\
| `url` | string | _search URL with refinement parameters_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `options` | array | _further search refinement options_ |  |\
| `type` | string | _type of element = **‘refinement\_chips\_option’**_ |  |\
| `title` | string | _title of the element_ |  |\
| `url` | string | _search URL with refinement parameters_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `item_types` | array | _types of search results in SERP_<br>contains types of search results ( `items`) found in SERP.<br>possible item types:<br>[`answer_box`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#answer_box), [`app`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#app), [`carousel`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#carousel), [`multi_carousel`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#multi_carousel), [`featured_snippet`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#featured_snippet), [`google_flights`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#google_flights), [`google_reviews`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#google_reviews), [`third_party_reviews`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#third_party_reviews), [`google_posts`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#google_posts), [`images`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#images), [`jobs`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#jobs), [`knowledge_graph`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#knowledge_graph), [`local_pack`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#local_pack), [`hotels_pack`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#hotels_pack), [`map`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#map), [`organic`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#organic), [`paid`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#paid), [`people_also_ask`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#people_also_ask), [`related_searches`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#related_searches), [`people_also_search`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#people_also_search), [`shopping`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#shopping), [`top_stories`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#top_stories), [`twitter`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#twitter), [`video`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#video), [`events`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#events), [`mention_carousel`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#mention_carousel), [`recipes`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#recipes), [`top_sights`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#top_sights), [`scholarly_articles`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#scholarly_articles), [`popular_products`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#popular_products), [`podcasts`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#podcasts), [`questions_and_answers`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#questions_and_answers), [`find_results_on`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#find_results_on), [`stocks_box`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#stocks_box), [`visual_stories`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#visual_stories), [`commercial_units`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#commercial_units), [`local_services`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#local_services), [`google_hotels`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#google_hotels), [`math_solver`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#math_solver), [`currency_box`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#currency_box), [`product_considerations`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#product_considerations), [`found_on_web`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#found_on_web), [`short_videos`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#short_videos), [`refine_products`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#refine_products), [`explore_brands`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#explore_brands), [`perspectives`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#perspectives), [`discussions_and_forums`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#discussions_and_forums), [`compare_sites`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#compare_sites), [`courses`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#courses), [`ai_overview`](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#ai_overview) |  |\
| `se_results_count` | integer | _total number of results in SERP_ |  |\
| `pages_count` | integer | _total search results pages retrieved_<br>total number of retrieved SERPs in the result |  |\
| `items_count` | integer | _the number of results returned in the **`items`** array_ |  |\
| **`items`** | array | _elements of search results found in SERP_ |  |\
| **[‘organic’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-organic-1.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘organic’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `url` | string | _relevant URL in SERP_ |  |\
| `cache_url` | string | _cached version of the page_ |  |\
| `related_search_url` | string | _URL to a similar search_<br>URL to a new search for the same keyword(s) [on related sites](https://support.google.com/websearch/answer/2466433?hl=en#:~:text=Search%20for%20related%20sites) |  |\
| `breadcrumb` | string | _breadcrumb in SERP_ |  |\
| `website_name` | string | _name of the website in SERP_ |  |\
| `is_image` | boolean | _indicates whether the element contains an `image`_ |  |\
| `is_video` | boolean | _indicates whether the element contains a `video`_ |  |\
| `is_featured_snippet` | boolean | _indicates whether the element is a `featured_snippet`_ |  |\
| `is_malicious` | boolean | _indicates whether the element is marked as malicious_ |  |\
| `is_web_story` | boolean | _indicates whether the element is marked as Google web story_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `pre_snippet` | string | _includes additional information appended before the result description in SERP_ |  |\
| `extended_snippet` | string | _includes additional information appended after the result description in SERP_ |  |\
| `images` | array | _images of the element_ |  |\
| `type` | string | _type of element = ‘ **images\_element**‘_ |  |\
| `alt` | string | _alt tag of the image_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `amp_version` | boolean | _Accelerated Mobile Pages_<br>indicates whether an item has the Accelerated Mobile Page (AMP) version |  |\
| `rating` | object | _the item’s rating_<br>the popularity rate based on reviews and displayed in SERP |  |\
| `rating_type` | string | _the type of_ _rating_<br>here you can find the following elements: `Max5`, `Percents`, `CustomMax` |  |\
| `value` | float | _the value of the rating_ |  |\
| `votes_count` | integer | _the amount of_ _feedback_ |  |\
| `rating_max` | integer | _the maximum value for a `rating_type`_ |  |\
| `price` | object | _pricing details_<br>contains the pricing details of the product or service featured in the result |  |\
| `current` | float | _current price_<br>indicates the current price of the product or service featured in the result |  |\
| `regular` | float | _regular price_<br>indicates the regular price of the product or service with no discounts applied |  |\
| `max_value` | float | _the maximum price_<br>the maximum price of the product or service as indicated in the result |  |\
| `currency` | string | _currency of the listed price_<br>ISO code of the currency applied to the price |  |\
| `is_price_range` | boolean | _price is provided as a range_<br>indicates whether a price is provided in a range |  |\
| `displayed_price` | string | _price string in the result_<br>raw price string as provided in the result |  |\
| `highlighted` | array | _words highlighted in bold within the results `description`_ |  |\
| `links` | array | _sitelinks_<br>the links shown below some of Google’s search results<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `url` | string | _sitelink URL_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `faq` | object | _frequently asked questions_<br>questions and answers extension shown below some of Google’s search results<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **faq\_box**‘_ |  |\
| `items` | array | _items featured in the faq\_box_ |  |\
| `type` | string | _type of element = ‘ **faq\_box\_element**‘_ |  |\
| `title` | string | _question related to the result_ |  |\
| `description` | string | _answer provided in the drop-down block_ |  |\
| `links` | array | _links featured in the faq\_box\_element_ |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _link anchor text_ |  |\
| `url` | string | _link URL_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `extended_people_also_search` | array | _extension of the organic element_<br>extension of the organic result containing related search queries<br>**Note:** extension appears in SERP upon clicking on the result and then bouncing back to search results |  |\
| `about_this_result` | object | _contains information from the ‘About this result’ panel_<br>[‘About this result’ panel](https://blog.google/products/search/learn-more-and-get-more-from-search/) provides additional context about why Google returned this result for the given query;<br>this feature appears after clicking on the three dots next to most results |  |\
| `type` | string | _type of element = ‘ **about\_this\_result\_element**‘_ |  |\
| `url` | string | _result’s URL_ |  |\
| `source` | string | _source of additional information about the result_ |  |\
| `source_info` | string | _additional information about the result_<br>description of the website from Wikipedia or another additional context |  |\
| `source_url` | string | _URL to full information from the `source`_ |  |\
| `language` | string | _the language of the result_ |  |\
| `location` | string | _location for which the result is relevant_ |  |\
| `search_terms` | array | _matching search terms that appear in the result_ |  |\
| `related_terms` | array | _related search terms that appear in the result_ |  |\
| `related_result` | array | _related result from the same domain_<br>related result from the same domain appears as a part of the main result snippet;<br>you can derive the `related_result` snippets as `"type": "organic"` results by setting the `group_organic_results` parameter to `false` in the POST request |  |\
| `type` | string | _type of element = ‘ **related\_result**‘_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `domain` | string | _relevant domain_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `url` | string | _relevant URL in SERP_ |  |\
| `cache_url` | string | _cached version of the page_ |  |\
| `related_search_url` | string | _URL to a similar search_<br>URL to a new search for the same keyword(s) [on related sites](https://support.google.com/websearch/answer/2466433?hl=en#:~:text=Search%20for%20related%20sites) |  |\
| `breadcrumb` | string | _breadcrumb in SERP_ |  |\
| `is_image` | boolean | _indicates whether the element contains an `image`_ |  |\
| `is_video` | boolean | _indicates whether the element contains a `video`_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `pre_snippet` | string | _includes additional information appended before the result description in SERP_ |  |\
| `extended_snippet` | string | _includes additional information appended after the result description in SERP_ |  |\
| `images` | array | _images of the element_ |  |\
| `type` | string | _type of element = ‘ **images\_element**‘_ |  |\
| `alt` | string | _alt tag of the image_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `amp_version` | boolean | _Accelerated Mobile Pages_<br>indicates whether an item has the Accelerated Mobile Page (AMP) version |  |\
| `rating` | object | _the item’s rating_<br>the popularity rate based on reviews and displayed in SERP |  |\
| `rating_type` | string | _the type of_ _rating_<br>here you can find the following elements: `Max5`, `Percents`, `CustomMax` |  |\
| `value` | float | _the value of the rating_ |  |\
| `votes_count` | integer | _the amount of_ _feedback_ |  |\
| `rating_max` | integer | _the maximum value for a `rating_type`_ |  |\
| `price` | object | _pricing details_<br>contains the pricing details of the product or service featured in the result |  |\
| `current` | float | _current price_<br>indicates the current price of the product or service featured in the result |  |\
| `regular` | float | _regular price_<br>indicates the regular price of the product or service with no discounts applied |  |\
| `max_value` | float | _the maximum price_<br>the maximum price of the product or service as indicated in the result |  |\
| `currency` | string | _currency of the listed price_<br>ISO code of the currency applied to the price |  |\
| `is_price_range` | boolean | _price is provided as a range_<br>indicates whether a price is provided in a range |  |\
| `displayed_price` | string | _price string in the result_<br>raw price string as provided in the result |  |\
| `highlighted` | array | _words highlighted in bold within the results `description`_ |  |\
| `about_this_result` | object | _contains information from the ‘About this result’ panel_<br>[‘About this result’ panel](https://blog.google/products/search/learn-more-and-get-more-from-search/) provides additional context about why Google returned this result for the given query;<br>this feature appears after clicking on the three dots next to most results |  |\
| `type` | string | _type of element = ‘ **about\_this\_result\_element**‘_ |  |\
| `url` | string | _result’s URL_ |  |\
| `source` | string | _source of additional information about the result_ |  |\
| `source_info` | string | _additional information about the result_<br>description of the website from Wikipedia or another additional context |  |\
| `source_url` | string | _URL to full information from the `source`_ |  |\
| `language` | string | _the language of the result_ |  |\
| `location` | string | _location for which the result is relevant_ |  |\
| `search_terms` | array | _matching search terms that appear in the result_ |  |\
| `related_terms` | array | _related search terms that appear in the result_ |  |\
| `timestamp` | string | _date and time when the result was published_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `timestamp` | string | _date and time when the result was published_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘paid’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-paid-1.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘paid’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `domain` | string | _domain in SERP of the ad element_ |  |\
| `website_name` | string | _name of the website in the ad element_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `url` | string | _relevant URL of the Ad element in SERP_ |  |\
| `breadcrumb` | string | _breadcrumb of the Ad element in SERP_ |  |\
| `is_image` | boolean | _indicates whether the element contains an `image`_ |  |\
| `is_video` | boolean | _indicates whether the element contains a `video`_ |  |\
| `images` | array | _images of the element_ |  |\
| `type` | string | _type of element = ‘ **images\_element**‘_ |  |\
| `alt` | string | _alt tag of the image_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `highlighted` | array | _words highlighted in bold within the results `description`_ |  |\
| `extra` | object | _additional information about the result_ |  |\
| `ad_aclk` | string | _the identifier of the ad_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `description_rows` | array | _extended description_<br>if there is none, equals `null` |  |\
| `links` | array | _sitelinks_<br>the links shown below some of Google’s search results<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of the link element_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `url` | string | _URL link_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `ad_aclk` | string | _the identifier of the ad_ |  |\
| `price` | object | _pricing details_<br>contains the pricing details of the product or service featured in the result |  |\
| `current` | float | _current price_<br>indicates the current price of the product or service featured in the result |  |\
| `regular` | float | _regular price_<br>indicates the regular price of the product or service with no discounts applied |  |\
| `max_value` | float | _the maximum price_<br>the maximum price of the product or service as indicated in the result |  |\
| `currency` | string | _currency of the listed price_<br>ISO code of the currency applied to the price |  |\
| `is_price_range` | boolean | _price is provided as a range_<br>indicates whether a price is provided in a range |  |\
| `displayed_price` | string | _price string in the result_<br>raw price string as provided in the result |  |\
| `rating` | object | _the element’s rating_<br>the popularity rate based on reviews and displayed in SERP |  |\
| `rating_type` | string | _the type of_ _rating_<br>here you can find the following elements: `Max5`, `Percents`, `CustomMax` |  |\
| `value` | float | _the value of the rating_ |  |\
| `votes_count` | integer | _the amount of_ _feedback_ |  |\
| `rating_max` | integer | _the maximum value for a `rating_type`_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘carousel’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-carousel-1.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘carousel’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **carousel\_element**‘_ |  |\
| `title` | string | _title of the item_ |  |\
| `subtitle` | string | _subtitle of the item_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘multi\_carousel’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/05/mobile-element-multi-carousel.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘multi\_carousel’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **multi\_carousel\_element**‘_ |  |\
| `title` | string | _title of the item_ |  |\
| `multi_carousel_snippets` | array | _`multi_carousel_snippet` results_ |  |\
| `type` | string | _type of element = ‘ **multi\_carousel\_snippet**‘_ |  |\
| `title` | string | _title of a particular item_ |  |\
| `subtitle` | string | _subtitle of the item_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘answer\_box’ element in SERP![](https://dataforseo.com/wp-content/uploads/2023/10/Answer_box-img.webp)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘answer\_box’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `text` | array | _text_<br>if there is none, equals `null` |  |\
| `links` | array | _sitelinks_<br>the links shown below some of Google’s search results<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of the link_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `url` | string | _URL link_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘related\_searches’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-related-searches.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘related\_searches’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘people\_also\_search’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-people-also-search.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘people\_also\_search’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘local\_pack’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-local-pack.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘local\_pack’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `phone` | string | _phone number_ |  |\
| `url` | string | _relevant URL_ |  |\
| `is_paid` | boolean | _indicates whether the element is an ad_ |  |\
| `rating` | object | _the item’s rating_<br>the popularity rate based on reviews and displayed in SERP |  |\
| `rating_type` | string | _the type of rating_<br>here you can find the following elements: `Max5`, `Percents`, `CustomMax` |  |\
| `value` | float | _the value of the rating_ |  |\
| `votes_count` | integer | _the amount of_ _feedback_ |  |\
| `rating_max` | integer | _the maximum value for a `rating_type`_ |  |\
| `cid` | string | _google-defined client id_<br>unique id of a local establishment;<br>can be used with [Google Reviews API](https://docs.dataforseo.com/v3/reviews/google/overview/?php) to get a full list of reviews |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘hotels\_pack’ element in SERP![](https://dataforseo.com/wp-content/uploads/2021/03/window-feature-hotel-1.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘hotels\_pack’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `date_from` | string | _starting date of stay_<br>in the format “year-month-date”<br>example:<br>2019-11-15 |  |\
| `date_to` | string | _ending date of stay_<br>in the format “year-month-date”<br>example:<br>2019-11-17 |  |\
| `items` | array | _contains results featured in the ‘hotels\_pack’ element of SERP_ |  |\
| `type` | string | _type of element = **‘hotels\_pack\_element’**_ |  |\
| `price` | object | _price of booking a place for the specified dates of stay_ |  |\
| `current` | float | _current price_<br>indicates the current price of booking a place for the specified dates of stay |  |\
| `regular` | float | _regular price_<br>indicates the regular price of booking a place for the specified dates of stay |  |\
| `max_value` | float | _the maximum price_<br>the maximum price of booking a place for the specified dates of stay |  |\
| `currency` | string | _currency of the listed price_<br>ISO code of the currency applied to the price |  |\
| `is_price_range` | boolean | _price is provided as a range_<br>indicates whether a price is provided in a range |  |\
| `displayed_price` | string | _price string in the result_<br>raw price string as provided in the result |  |\
| `title` | string | _title of the place_ |  |\
| `desription` | string | _description of the place in SERP_ |  |\
| `hotel_identifier` | string | _unique hotel identifier_<br>unique hotel identifier assigned by Google;<br>example: `"CgoIjaeSlI6CnNpVEAE"` |  |\
| `domain` | string | _domain in SERP_ |  |\
| `url` | string | _relevant URL_ |  |\
| `is_paid` | boolean | _indicates whether the element is an ad_ |  |\
| `rating` | object | _the item’s rating_<br>the popularity rate based on reviews and displayed in SERP |  |\
| `rating_type` | string | _the type of rating_<br>here you can find the following elements: `Max5`, `Percents`, `CustomMax` |  |\
| `value` | float | _the value of the rating_ |  |\
| `votes_count` | integer | _the amount of_ _feedback_ |  |\
| `rating_max` | integer | _the maximum value for a `rating_type`_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘knowledge\_graph’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-Knowledge-Graph-2.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  | **note** that `knowledge_graph` items in `mobile` results may be separated by other elements;<br>in such cases, the API response returns several `knowledge_graph` elements, each containing distinct items, and each placed according to the items’ placement in SERP |  |\
| `type` | string | _type of element = **‘knowledge\_graph’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `subtitle` | string | _subtitle of the item_ |  |\
| `description` | string | _description_ |  |\
| `card_id` | string | _card id_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image from knowledge graph_ |  |\
| `logo_url` | string | _URL of the logo from knowledge graph_ |  |\
| `cid` | string | _google-defined client id_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_images\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `link` | object | _link of the element_ |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of a given link element_ |  |\
| `url` | string | _URL_ |  |\
| `domain` | string | _domain where a link points_ |  |\
| `snippet` | string | _text alongside the link title_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _contains arrays of specific images_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_images\_element**‘_ |  |\
| `url` | string | _image source URL_ |  |\
| `domain` | string | _website domain_ |  |\
| `alt` | string | _alt attribute_ |  |\
| `image_url` | string | _URL of a specific image_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_list\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the element_ |  |\
| `data_attrid` | string | _google defined data attribute ID_<br>example:<br>`action:listen_artist` |  |\
| `link` | object | _link of the element_ |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of a given link element_ |  |\
| `url` | string | _URL_ |  |\
| `domain` | string | _domain where a link points_ |  |\
| `snippet` | string | _text alongside the link title_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _contains arrays of elements available in the list_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_list\_element**‘_ |  |\
| `title` | string | _title of the element_ |  |\
| `subtitle` | string | _subtitle of the element_ |  |\
| `url` | string | _URL of element_ |  |\
| `domain` | string | _website domain_ |  |\
| `image_url` | string | _URL of the image_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_ai\_overview\_item‘**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `asynchronous_ai_overview` | boolean | _indicates whether the element is loaded asynchronically_<br>if `true`, the `ai_overview` element is loaded asynchronically;<br>if `false`, the `ai_overview` element is loaded from cache; |  |\
| `items` | array | _items present in the element_ |  |\
| `type` | string | _type of element = ‘ **ai\_overview\_element**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `title` | string | _title of the element_ |  |\
| `text` | string | _text or description of the element in SERP_ |  |\
| `markdown` | string | _content of the element in markdown format_ |  |\
| `links` | array | _website links featured in the element_ |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _link anchor text_ |  |\
| `description` | string | _link description_ |  |\
| `url` | string | _link URL_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `images` | array | _images of the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **images\_element**‘_ |  |\
| `alt` | string | _alt tag of the image_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `references` | array | _references relevant to the element_<br>includes references to webpages that were used to generate the `ai_overview_element` |  |\
| `type` | string | _type of element = ‘ **ai\_overview\_reference**‘_ |  |\
| `source` | string | _reference source name or title_ |  |\
| `domain` | string | _domain name of the reference_ |  |\
| `url` | string | _reference page URL_ |  |\
| `title` | string | _reference page title_ |  |\
| `text` | string | _reference text_<br>text snippet from the page that was used to generate the `ai_overview_element` |  |\
| `type` | string | _type of element = ‘ **ai\_overview\_video\_element**‘_ |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `title` | string | _title of the element_ |  |\
| `snippet` | string | _additional information for the video_ |  |\
| `url` | string | _URL of the link to the video_ |  |\
| `domain` | string | _domain of the website hosting the video_ |  |\
| `image_url` | string | _URL to the image thumbnail of the video_ |  |\
| `source` | string | _name of the source of the video_ |  |\
| `date` | string | _date when the video was published or indexed_<br>example:<br>`Apr 26, 2024` |  |\
| `timestamp` | string | _date and time when the video was published or indexed_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `type` | string | _type of element = ‘ **ai\_overview\_table\_element**‘_ |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `markdown` | string | _content of the element in markdown format_ |  |\
| `table` | object | _table present in the element_<br>the header and content of the table present in the element |  |\
| `table_header` | array | _content in the header of the table_ |  |\
| `table_content` | array | _array of contents of the table present in the element_<br>each array represents the table row |  |\
| `references` | array | _references relevant to the element_<br>includes references to webpages that were used to generate the `ai_overview_element` |  |\
| `type` | string | _type of element = ‘ **ai\_overview\_reference**‘_ |  |\
| `source` | string | _reference source name or title_ |  |\
| `domain` | string | _domain name of the reference_ |  |\
| `url` | string | _reference page URL_ |  |\
| `title` | string | _reference page title_ |  |\
| `text` | string | _reference text_<br>text snippet from the page that was used to generate the `ai_overview_element` |  |\
| `type` | string | _type of element = ‘ **ai\_overview\_expanded\_element**‘_ |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `title` | string | _title of the element in SERP_ |  |\
| `text` | string | _additional text of the element in SERP_ |  |\
| `components` | array | _array of components of the element_ |  |\
| `type` | string | _type of component = ‘ **ai\_overview\_expanded\_component**‘_ |  |\
| `title` | string | _title of the element in SERP_ |  |\
| `text` | string | _text of the component_ |  |\
| `markdown` | string | _text of the component in the markdwon format_ |  |\
| `images` | array | _images of the component_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **images\_element**‘_ |  |\
| `alt` | string | _alt tag of the image_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `links` | array | _sitelinks_<br>the links shown below some of Google’s search results<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of the link_ |  |\
| `description` | string | _description of the link_ |  |\
| `url` | string | _URL in link_ |  |\
| `domain` | string | _domain in link_ |  |\
| `references` | array | _additional references relevant to the item_<br>includes references to webpages that may have been used to generate the `ai_overview` |  |\
| `type` | string | _type of element = ‘ **ai\_overview\_reference**‘_ |  |\
| `source` | string | _reference source name or title_ |  |\
| `domain` | string | _domain name of the reference_ |  |\
| `url` | string | _reference page URL_ |  |\
| `title` | string | _reference page title_ |  |\
| `text` | string | _reference text_<br>text snippet from the page that was used to generate the `ai_overview_element` |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| ``**type** | string | _type of element = ‘ **knowledge\_graph\_description\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `text` | string | _description content_ |  |\
| `links` | array | _link of the element_ |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of a given link element_ |  |\
| `url` | string | _URL_ |  |\
| `domain` | string | _domain where a link points_ |  |\
| `snippet` | string | _text alongside the link title_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| ``**type** | string | _type of element = ‘ **knowledge\_graph\_row\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the row_ |  |\
| `data_attrid` | string | _google defined data attribute ID_<br>example:<br>`ss:/webfacts:net_worth` |  |\
| `text` | string | _row content_ |  |\
| `links` | array | _link of the element_ |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of a given link element_ |  |\
| `url` | string | _URL_ |  |\
| `domain` | string | _domain where a link points_ |  |\
| `snippet` | string | _text alongside the link title_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| ``**type** | string | _type of element = ‘ **knowledge\_graph\_carousel\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the carousel item_ |  |\
| `data_attrid` | string | _google defined data attribute ID_<br>example:<br>`kc:/common/topic:social media presence` |  |\
| `link` | object | _link of the element_ |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of a given link element_ |  |\
| `url` | string | _URL_ |  |\
| `domain` | string | _domain where a link points_ |  |\
| `snippet` | string | _text alongside the link title_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _contains arrays of elements available in the list_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_carousel\_element**‘_ |  |\
| `title` | string | _title of the element_ |  |\
| `subtitle` | string | _subtitle of the element_ |  |\
| `url` | string | _URL of element_ |  |\
| `domain` | string | _website domain_ |  |\
| `image_url` | string | _URL of the image_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| ``**type** | string | _type of element = ‘ **knowledge\_graph\_part\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the item_ |  |\
| `data_attrid` | string | _google defined data attribute ID_<br>example:<br>`kc:/local:place qa` |  |\
| `text` | string | _content within the item_ |  |\
| `links` | array | _link of the element_ |  |\
| `type` | string | _type of element = ‘ **link\_element**‘_ |  |\
| `title` | string | _title of a given link element_ |  |\
| `url` | string | _URL_ |  |\
| `domain` | string | _domain where a link points_ |  |\
| `snippet` | string | _text alongside the link title_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| ``**type** | string | _type of element = ‘ **knowledge\_graph\_expanded\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the item_ |  |\
| `data_attrid` | string | _google defined data attribute ID_<br>example:<br>`kc:/local:place qa` |  |\
| `expanded_element` | array | _link of the element_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_expanded\_element**‘_ |  |\
| `featured_title` | string | _title of a given element_ |  |\
| `url` | string | _source URL_ |  |\
| `domain` | string | _source domain_ |  |\
| `title` | string | _source title_ |  |\
| `snippet` | string | _text alongside the title_ |  |\
| `timestamp` | string | _date and time when the result was published_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `images` | array | _images of the element_ |  |\
| `type` | string | _type of element = ‘ **images\_element**‘_ |  |\
| `alt` | string | _alt tag of the image_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `table` | object | _table element_ |  |\
| `table_element` | string | _name assigned to the table element_<br>possible values:<br>`table_element` |  |\
| `table_header` | array | _column names_ |  |\
| `table_content` | array | _the content of the table_<br>one line of the table in this element of the array |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| ``**type** | string | _type of element = ‘ **knowledge\_graph\_shopping\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the item_ |  |\
| `data_attrid` | string | _google defined data attribute ID_<br>example:<br>`kc:/shopping/gpc:organic-offers` |  |\
| `items` | array | _link of the element_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_shopping\_element**‘_ |  |\
| `title` | string | _title of a given shopping element_ |  |\
| `url` | string | _URL_ |  |\
| `domain` | string | _domain in url_ |  |\
| `price` | object | _price indicated in the element_ |  |\
| `current` | float | _current price_<br>refers to the current price indicated in the element |  |\
| `regular` | float | _regular price_<br>refers to the regular price indicated in the element |  |\
| `max_value` | float | _the maximum price_<br>refers to the maximum price indicated in the element |  |\
| `currency` | string | _currency of the listed price_<br>ISO code of the currency applied to the price |  |\
| `is_price_range` | boolean | _price is provided as a range_<br>indicates whether a price is provided in a range |  |\
| `displayed_price` | string | _price string in the result_<br>raw price string as provided in the result |  |\
| `source` | string | _web source of the shopping element_<br>indicates the source of information included in the element |  |\
| `snippet` | string | _description of the shopping element_ |  |\
| `marketplace` | string | _merchant account provider_<br>ecommerce site that hosts products or websites of individual sellers under the same merchant account<br>example:<br>`by Google` |  |\
| `marketplace_url` | string | _URL to the merchant account provider_<br>ecommerce site that hosts products or websites of individual sellers under the same merchant account |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_hotels\_booking\_item**‘_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values;<br>positions of elements with different `type` values are omitted from `rank_group`;<br>always equals `0` for `desktop` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP<br>always equals `0` for `desktop` |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the element_ |  |\
| `date_from` | string | _starting date of stay_<br>in the format “year-month-date”<br>example:<br>2019-11-15 |  |\
| `date_to` | string | _ending date of stay_<br>in the format “year-month-date”<br>example:<br>2019-11-17 |  |\
| `data_attrid` | string | _google defined data attribute ID_<br>example:<br>`kc:/local:hotel booking` |  |\
| `items` | array | _contains arrays of elements available in the list_ |  |\
| `type` | string | _type of element = ‘ **knowledge\_graph\_hotels\_booking\_element**‘_ |  |\
| `source` | string | _web source of the hotel booking element_<br>indicates the source of information included in the element |  |\
| `description` | string | _description of the hotel booking element_ |  |\
| `url` | string | _URL_ |  |\
| `domain` | string | _domain in the URL_ |  |\
| `price` | object | _price indicated in the element_ |  |\
| `current` | float | _current price_<br>refers to the current price indicated in the element |  |\
| `regular` | float | _regular price_<br>refers to the regular price indicated in the element |  |\
| `max_value` | float | _the maximum price_<br>refers to the maximum price indicated in the element |  |\
| `currency` | string | _currency of the listed price_<br>ISO code of the currency applied to the price |  |\
| `is_price_range` | boolean | _price is provided as a range_<br>indicates whether a price is provided in a range |  |\
| `displayed_price` | string | _price string in the result_<br>raw price string as provided in the result |  |\
| `is_paid` | boolean | _indicates whether the element is an ad_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘featured\_snippet’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-featured_snippet.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘featured\_snippet’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `featured_title` | string | _the title of the featured snippets source page_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `timestamp` | string | _date and time when the result was published_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `url` | string | _relevant URL_ |  |\
| `images` | array | _images of the element_ |  |\
| `type` | string | _type of element = ‘ **images\_element**‘_ |  |\
| `alt` | string | _alt tag of the image_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `table` | object | _results table_<br>if there are none, equals `null` |  |\
| `table_header` | array | _column names_ |  |\
| `table_content` | array | _the content of the table_<br>one line of the table in this element of the array |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘top\_stories’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-top-stories.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘top\_stories’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `page` | integer | _search results page number_<br>indicates the number of the SERP page on which the element is located |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the element in SERP_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **top\_stories\_element**‘_ |  |\
| `source` | string | _source of the element_<br>indicates the source of information included in the `top_stories_element` |  |\
| `domain` | string | _domain in SERP_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `date` | string | _the date when the page source of the element was published_ |  |\
| `amp_version` | boolean | _Accelerated Mobile Pages_<br>indicates whether an item has the Accelerated Mobile Page (AMP) version |  |\
| `timestamp` | string | _date and time when the result was published_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `url` | string | _URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available) |  |\
| `badges` | array | _badges relevant to the element_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘twitter’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-twitters.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘twitter’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `url` | string | _URL_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **twitter** **\_element**‘_ |  |\
| `tweet` | string | _tweet message_ |  |\
| `date` | string | _the posting date_ |  |\
| `timestamp` | string | _date and time when the result was published_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `url` | string | _URL_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘map’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-map.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘map’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `url` | string | _URL_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘google\_flights’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-google-flights.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘google\_flights’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `url` | string | _URL_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **google\_flights\_element**‘_ |  |\
| `description` | string | _description_ |  |\
| `url` | string | _URL_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘google\_reviews’ element in SERP![](https://dataforseo.com/wp-content/uploads/2021/03/desktop-element-google_reviews.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘google\_reviews’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `reviews_count` | integer | _the number of reviews_ |  |\
| `rating` | object | _the element’s rating_<br>the popularity rate based on reviews and displayed in SERP |  |\
| `rating_type` | string | _the type of_ _rating_<br>here you can find the following elements: `Max5`, `Percents`, `CustomMax` |  |\
| `value` | integer | _the value of the rating_ |  |\
| `votes_count` | integer | _the amount of_ _feedback_ |  |\
| `rating_max` | integer | _the maximum value for a `rating_type`_ |  |\
| `place_id` | string | _the identifier of a place_ |  |\
| `feature` | string | _the additional feature of the review_ |  |\
| `cid` | string | _google-defined client id_<br>unique id of a local establishment;<br>can be used with [Google Reviews API](https://docs.dataforseo.com/v3/reviews/google/overview/?php) to get a full list of reviews |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘third\_party\_reviews’ element in SERP![](https://docs.dataforseo.com/wp-content/uploads/2025/02/external_reviews.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘third\_party\_reviews’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `reviews_count` | integer | _the number of reviews_ |  |\
| `title` | string | _name of the third-party review source_ |  |\
| `url` | string | _URL of the third-party review source_ |  |\
| `rating` | object | _the element’s rating_<br>the popularity rate based on reviews and displayed in SERP |  |\
| `rating_type` | string | _the type of_ _rating_<br>here you can find the following elements: `Max5`, `Percents`, `CustomMax` |  |\
| `value` | integer | _the value of the rating_ |  |\
| `votes_count` | integer | _the amount of_ _feedback_ |  |\
| `rating_max` | integer | _the maximum value for a `rating_type`_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘google\_posts’ element in SERP![](https://dataforseo.com/wp-content/uploads/2021/03/desktop-element-google_posts.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘google\_posts’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `posts_id` | string | _the identifier of the google\_posts feature_ |  |\
| `feature` | string | _the additional feature of the review_ |  |\
| `cid` | string | _google-defined client id_<br>unique id of a local establishment;<br>can be used with [Google Reviews API](https://docs.dataforseo.com/v3/reviews/google/overview/?php) to get a full list of reviews |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘video’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-video.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘video’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **video\_element**‘_ |  |\
| `source` | string | _source of the element_<br>indicates the source of the video |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `timestamp` | string | _date and time when the result was published_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |\
| `url` | string | _URL_ |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘app’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/05/mobile-element-app.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘app’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **app\_element**‘_ |  |\
| `description` | string | _description of the results element in SERP_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `url` | string | _URL_ |  |\
| `price` | object | _price of the app element_ |  |\
| `current` | float | _current price_<br>refers to the current price indicated in the app element |  |\
| `regular` | float | _regular price_<br>refers to the regular price indicated in the app element |  |\
| `max_value` | float | _the maximum price_<br>refers to the maximum price indicated in the app element |  |\
| `currency` | string | _currency of the listed price_<br>ISO code of the currency applied to the price |  |\
| `is_price_range` | boolean | _price is provided as a range_<br>indicates whether a price is provided in a range |  |\
| `displayed_price` | string | _price string in the result_<br>raw price string as provided in the result |  |\
| `rectangle` | object | _rectangle parameters_<br>contains cartesian coordinates and pixel dimensions of the result’s snippet in SERP<br>equals `null` if `calculate_rectangles` in the POST request is not set to `true` |  |\
| `x` | float | _x-axis coordinate_<br>x-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `y` | float | _y-axis coordinate_<br>y-axis coordinate of the top-left corner of the result’s snippet, where top-left corner of the screen is the origin |  |\
| `width` | float | _width of the element in pixels_ |  |\
| `height` | float | _height of the element in pixels_ |  |\
| **[‘people\_also\_ask’ element in SERP![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-paa.png)](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/#)** |  |  |  |\
| `type` | string | _type of element = **‘people\_also\_ask’**_ |  |\
| `rank_group` | integer | _group rank in SERP_<br>position within a group of elements with identical `type` values<br>positions of elements with different `type` values are omitted from `rank_group` |  |\
| `rank_absolute` | integer | _absolute rank in SERP_<br>absolute position among all the elements in SERP |  |\
| `position` | string | _the alignment of the element in SERP_<br>can take the following values:<br>`left`, `right` |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `items` | array | _additional items present in the element_<br>if there are none, equals `null` |  |\
| `type` | string | _type of element = ‘ **people\_also\_ask\_element**‘_ |  |\
| `title` | string | _title of the result in SERP_ |  |\
| `seed_question` | string | _question that triggered additional expanded elements_ |  |\
| `xpath` | string | _the [XPath](https://en.wikipedia.org/wiki/XPath) of the element_ |  |\
| `expanded_element` | array | _expanded element_ |  |\
| `type` | string | _type of element = ‘ **people\_also\_ask\_expanded\_element**‘_ |  |\
| `featured_title` | string | _title_ |  |\
| `url` | string | _relevant URL_ |  |\
| `domain` | string | _domain in SERP_ |  |\
| code>title | string | _title of the result in SERP_ |\
| `description` | string | _description of the results element in SERP_ |  |\
| `images` | array | _images of the element_ |  |\
| `type` | string | _type of element = ‘ **images\_element**‘_ |  |\
| `alt` | string | _alt tag of the image_ |  |\
| `url` | string | _relevant URL_ |  |\
| `image_url` | string | _URL of the image_<br>the URL leading to the image on the original |  |



## DataForSEO API v.3: OnPage API Instant Pages

This function allows you to retrieve page-specific data with detailed information on how well a particular page is optimized for organic search. This endpoint operates based on the **Live method**, meaning it does not require a separate GET request to obtain task results.

### API Endpoint

**POST `https://api.dataforseo.com/v3/on_page/instant_pages`**

Your account will be charged for each request made to this endpoint.

### Authentication

To authenticate, you should use your credentials from `https://app.dataforseo.com/api-access`.

You will need to encode your `login:password` combination using Base64 for the `Authorization` header.

**Example Authentication Header:**
`Authorization: Basic {base64_encoded_login:password}`

### Request Parameters

All POST data must be sent in **JSON format** with **UTF-8 encoding**. The task setting is done using the POST method, where all task parameters are sent within a `task` array of the generic POST array.

You can send up to **2000 API requests per minute**, with each request containing no more than **20 tasks**. The maximum number of simultaneous requests is limited to **30**. In a single request, you can set up to 20 tasks, each containing one URL, but these URLs cannot contain more than **5 identical domains**.

**Request Body Example:**

```json
[
{
  "url": "https://dataforseo.com/blog",
  "enable_javascript": true,
  "custom_js": "meta = {}; meta.url = document.URL; meta;"
}
]
```
_This example shows setting a task with additional parameters._

**Description of Fields for Setting a Task:**

| Field Name                   | Type      | Description                                                                                                                                                                                       |url|string|*target page url* **required field**
absolute URL of the target page;
**Note #1:** results will be returned for the specified URL only;
**Note #2:** to prevent denial-of-service events, tasks that contain a duplicate crawl host will be returned with a 40501 error;
to prevent this error from occurring, avoid setting tasks with the same domain if at least one of your previous tasks with this domain (including a page URL on the domain) is still in a crawling queue|
|`custom_user_agent`          |string     |*custom user agent* optional field
custom user agent for crawling a website
example: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36`
default value: `Mozilla/5.0 (compatible; RSiteAuditor)`|
|`browser_preset`             |string     |*preset for browser screen parameters* optional field
If you use this field, you do not need to indicate `browser_screen_width`, `browser_screen_height`, `browser_screen_scale_factor`.
Possible values: `desktop`, `mobile`, `tablet`
`desktop` preset will apply: `browser_screen_width: 1920`, `browser_screen_height: 1080`, `browser_screen_scale_factor: 1`
`mobile` preset will apply: `browser_screen_width: 390`, `browser_screen_height: 844`, `browser_screen_scale_factor: 3`
`tablet` preset will apply: `browser_screen_width: 1024`, `browser_screen_height: 1366`, `browser_screen_scale_factor: 2`
**Note:** To use this parameter, set `enable_javascript` or `enable_browser_rendering` to `true`|
|`browser_screen_width`       |integer    |*browser screen width* optional field
You can set a custom browser screen width to perform an audit for a particular device.
If you use this field, `browser_preset` will be ignored.
**Note:** To use this parameter, set `enable_javascript` or `enable_browser_rendering` to `true`.
Minimum value, in pixels: `240`
Maximum value, in pixels: `9999`|
|`browser_screen_height`      |integer    |*browser screen height* optional field
You can set a custom browser screen height to perform an audit for a particular device.
If you use this field, `browser_preset` will be ignored.
**Note:** To use this parameter, set `enable_javascript` or `enable_browser_rendering` to `true`.
Minimum value, in pixels: `240`
Maximum value, in pixels: `9999`|
|`browser_screen_scale_factor`|float      |*browser screen scale factor* optional field
You can set a custom browser screen resolution ratio to perform an audit for a particular device.
If you use this field, `browser_preset` will be ignored.
**Note:** To use this parameter, set `enable_javascript` or `enable_browser_rendering` to `true`.
Minimum value: `0.5`
Maximum value: `3`|
|`store_raw_html`             |boolean    |*store HTML of a crawled page* optional field
Set to `true` if you want to get the HTML of the page using the OnPage Raw HTML endpoint.
Default value: `false`|
|`accept_language`            |string     |*language header for accessing the website* optional field
All locale formats are supported (xx, xx-XX, xxx-XX, etc.).
**Note:** If you do not specify this parameter, some websites may deny access; in this case, pages will be returned with `"type":"broken"` in the response array|
|`load_resources`             |boolean    |*load resources* optional field
Set to `true` if you want to load images, stylesheets, scripts, and broken resources.
Default value: `false`
**Note:** If you use this parameter, additional charges will apply. The cost can be calculated on the Pricing Page|
|`enable_javascript`          |boolean    |*load javascript on a page* optional field
Set to `true` if you want to load the scripts available on a page.
Default value: `false`
**Note:** If you use this parameter, additional charges will apply. The cost can be calculated on the Pricing Page|
|`enable_browser_rendering`   |boolean    |*emulate browser rendering to measure Core Web Vitals* optional field
By using this parameter, you will be able to emulate a browser when loading a web page.
`enable_browser_rendering` loads styles, images, fonts, animations, videos, and other resources on a page.
Default value: `false`
Set to `true` to obtain Core Web Vitals (FID, CLS, LCP) metrics in the response.
**If you use this field, parameters `enable_javascript` and `load_resources` are enabled automatically.**
**Note:** If you use this parameter, additional charges will apply. The cost can be calculated on the Pricing Page|
|`disable_cookie_popup`       |boolean    |*disable the cookie popup* optional field
Set to `true` if you want to disable the popup requesting cookie consent from the user.
Default value: `false`|
|`return_despite_timeout`     |boolean    |*return data on pages despite the timeout error* optional field
If `true`, data will be provided on pages that failed to load within 120 seconds and responded with a timeout error.
Default value: `false`|
|`enable_xhr`                 |boolean    |*enable XMLHttpRequest on a page* optional field
Set to `true` if you want our crawler to request data from a web server using the XMLHttpRequest object.
Default value: `false`
**Note:** If you use this field, `enable_javascript` must be set to `true`|
|`custom_js`                  |string     |*custom javascript* optional field
The execution time for the script you enter here should be **700 ms maximum**.
For example, you can use a JS snippet to check if the website contains Google Tag Manager.
The returned value depends on what you specify. For instance, `meta = {}; meta.url = document.URL; meta.test = 'test'; meta;` will return `"custom_js_response": { "url": "https://dataforseo.com/", "test": "test" }`.
**Note:** If you use this parameter, additional charges will apply. The cost can be calculated on the Pricing Page|
|`validate_micromarkup`       |boolean    |*enable microdata validation* optional field
If set to `true`, you can use the OnPage API Microdata endpoint with the `id` of the task.
Default value: `false`|
|`check_spell`                |boolean    |*check spelling* optional field
Set to `true` to check spelling on a website using the Hunspell library.
Default value: `false`|
|`checks_threshold`           |array      |*custom threshold values for checks* optional field
You can specify custom threshold values for the parameters included in the `checks` array of OnPage API responses.
**Note:** Only integer threshold values can be modified|
|`switch_pool`                |boolean    |*switch proxy pool* optional field
If `true`, additional proxy pools will be used to obtain the requested data.
This parameter can be used if a multitude of tasks is set simultaneously, resulting in occasional `rate-limit` and/or `site_unreachable` errors|
|`ip_pool_for_scan`           |string     |*proxy pool* optional field
You can choose a location of the proxy pool that will be used to obtain the requested data.
This parameter can be used if page content is inaccessible in one of the locations, resulting in occasional `site_unreachable` errors.
Possible values: `us`, `de`|

### Response Parameters

As a response, the API server will return JSON-encoded data containing a `tasks` array with information specific to the set tasks.

**General Response Fields:**

| Field Name     | Type    | Description                                                                                                                                              |
| :------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `version`      | string  | **The current version of the API**.                                                                                                                 |
| `status_code`  | integer | **General status code** of the request. A full list of response codes is available.                                                            |
| `status_message` | string  | **General informational message**. A full list of general informational messages is available.                                                 |
| `time`         | string  | **Execution time**, in seconds.                                                                                                                     |
| `cost`         | float   | Total **cost of tasks**, in USD.                                                                                                                    |
| `tasks_count`  | integer | The number of tasks in the `tasks` array.                                                                                                           |
| `tasks_error`  | integer | The number of tasks in the `tasks` array that returned with an error.                                                                               |
| `tasks`        | array   | **Array of tasks**. Each element represents a task submitted in the POST request.                                                                   |

**Fields within the `tasks` Array (for each task):**

| Field Name     | Type    | Description                                                                                                                                              |
| :------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`           | string  | **Task identifier**, a unique UUID in our system.                                                                                                   |
| `status_code`  | integer | **Status code of the task**, generated by DataForSEO (range: 10000-60000).                                                                        |
| `status_message` | string  | **Informational message of the task**.                                                                                                            |
| `time`         | string  | **Execution time** for the task, in seconds.                                                                                                        |
| `cost`         | float   | **Cost of the task**, in USD.                                                                                                                       |
| `result_count` | integer | **Number of elements in the `result` array**.                                                                                                       |
| `path`         | array   | **URL path** for the API endpoint (e.g., `["v3", "on_page", "instant_pages"]`).                                                                 |
| `data`         | object  | **Contains the same parameters that you specified in the POST request**.                                                                        |
| `result`       | array   | **Array of results**.                                                                                                                           |

**Fields within the `result` Array:**

The `result` array contains items with different `resource_type` values, each having specific fields.

---

#### **`resource_type`: 'html' (for HTML pages)**

| Field Name                     | Type    | Description                                                                                                                                                                                                                                                                     |
| :----------------------------- | :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `crawl_progress`               | string  | **Status of the crawling session**. Possible values: `in_progress`, `finished`.                                                                                                                                                                                |
| `crawl_status`                 | object  | **Details of the crawling session**. In this case, the value will be `null`.                                                                                                                                                                                   |
| `crawl_gateway_address`        | string  | **Crawler IP address**. Displays the IP address used by the crawler to initiate the current crawling session.                                                                                                                                                 |
| `items_count`                  | integer | **Number of items** in the `items` array.                                                                                                                                                                                                                    |
| `items`                        | array   | **Items array**, representing the 'html' page.                                                                                                                                                                                                                 |
| `items.resource_type`          | string  | **Type of the returned resource**. Equals `'html'`.                                                                                                                                                                                                                |
| `items.status_code`            | integer | **Status code of the page** (e.g., 200).                                                                                                                                                                                                                       |
| `items.location`               | string  | **Location header**. Indicates the URL to redirect a page to.                                                                                                                                                                                                  |
| `items.url`                    | string  | **Page URL**.                                                                                                                                                                                                                                                  |
| `items.meta`                   | object  | **Page properties**.                                                                                                                                                                                                                                           |
| `items.meta.title`             | string  | **Page title**.                                                                                                                                                                                                                                                |
| `items.meta.charset`           | integer | **Code page** (e.g., 65001).                                                                                                                                                                                                                                   |
| `items.meta.follow`            | boolean | **Indicates whether a page’s ‘meta robots’ allows crawlers to follow the links on the page**. If `false`, the page’s ‘meta robots’ tag contains “nofollow”.                                                                                                 |
| `items.meta.generator`         | string  | **Meta tag generator**.                                                                                                                                                                                                                                        |
| `items.meta.htags`             | object  | **HTML header tags** (e.g., `h4`, `h1`, `h2` and their content).                                                                                                                                                                                              |
| `items.meta.description`       | string  | **Content of the meta description tag**.                                                                                                                                                                                                                       |
| `items.meta.favicon`           | string  | **Favicon of the page**.                                                                                                                                                                                                                                       |
| `items.meta.meta_keywords`     | string  | **Content of the `keywords` meta tag**.                                                                                                                                                                                                                        |
| `items.meta.canonical`         | string  | **Canonical page URL**.                                                                                                                                                                                                                                        |
| `items.meta.internal_links_count` | integer | **Number of internal links** on the page.                                                                                                                                                                                                                      |
| `items.meta.external_links_count` | integer | **Number of external links** on the page.                                                                                                                                                                                                                      |
| `items.meta.inbound_links_count` | integer | **Number of internal links pointing at the page**.                                                                                                                                                                                                             |
| `items.meta.images_count`      | integer | **Number of images** on the page.                                                                                                                                                                                                                              |
| `items.meta.images_size`       | integer | **Total size of images** on the page measured in bytes.                                                                                                                                                                                                        |
| `items.meta.scripts_count`     | integer | **Number of scripts** on the page.                                                                                                                                                                                                                             |
| `items.meta.scripts_size`      | integer | **Total size of scripts** on the page measured in bytes.                                                                                                                                                                                                       |
| `items.meta.stylesheets_count` | integer | **Number of stylesheets** on the page.                                                                                                                                                                                                                         |
| `items.meta.stylesheets_size`  | integer | **Total size of stylesheets** on the page measured in bytes.                                                                                                                                                                                                   |
| `items.meta.title_length`      | integer | **Length of the `title` tag** in characters.                                                                                                                                                                                                                   |
| `items.meta.description_length` | integer | **Length of the `description` tag** in characters.                                                                                                                                                                                                             |
| `items.meta.render_blocking_scripts_count` | integer | **Number of scripts on the page that block page rendering**.                                                                                                                                                                                           |
| `items.meta.render_blocking_stylesheets_count` | integer | **Number of CSS styles on the page that block page rendering**.                                                                                                                                                                                  |
| `items.meta.cumulative_layout_shift` | float | **Core Web Vitals metric measuring the layout stability of the page**. Sum total of all individual layout shift scores for every unexpected layout shift during the page's lifespan.                                                                       |
| `items.meta.meta_title`        | string  | **Meta title of the page**. The meta tag in the head section of an HTML document that defines the title of a page.                                                                                                                                              |
| `items.meta.content`           | object  | **Overall information about content of the page**.                                                                                                                                                                                                             |
| `items.meta.content.plain_text_size` | integer | **Total size of the text** on the page measured in bytes.                                                                                                                                                                                                      |
| `items.meta.content.plain_text_rate` | integer | **Plaintext rate value**. `plain_text_size` to `size` ratio.                                                                                                                                                                                                   |
| `items.meta.content.plain_text_word_count` | float | **Number of words** on the page.                                                                                                                                                                                                                               |
| `items.meta.content.automated_readability_index` | float | **Automated Readability Index**.                                                                                                                                                                                                                             |
| `items.meta.content.coleman_liau_readability_index` | float | **Coleman–Liau Index**.                                                                                                                                                                                                                                        |
| `items.meta.content.dale_chall_readability_index` | float | **Dale–Chall Readability Index**.                                                                                                                                                                                                                              |
| `items.meta.content.flesch_kincaid_readability_index` | float | **Flesch–Kincaid Readability Index**.                                                                                                                                                                                                                          |
| `items.meta.content.smog_readability_index` | float | **SMOG Readability Index**.                                                                                                                                                                                                                                |
| `items.meta.content.description_to_content_consistency` | float | **Consistency of the meta `description` tag with the page content**, measured from 0 to 1.                                                                                                                                                                 |
| `items.meta.content.title_to_content_consistency` | float | **Consistency of the meta `title` tag with the page content**, measured from 0 to 1.                                                                                                                                                                       |
| `items.meta.content.meta_keywords_to_content_consistency` | float | **Consistency of meta `keywords` tag with the page content**, measured from 0 to 1.                                                                                                                                                                |
| `items.meta.deprecated_tags`   | array   | **Deprecated tags** on the page.                                                                                                                                                                                                                               |
| `items.meta.duplicate_meta_tags` | array   | **Duplicate meta tags** on the page (e.g., "generator").                                                                                                                                                                                                         |
| `items.meta.spell`             | object  | **Spellcheck** results, including Hunspell spellcheck errors.                                                                                                                                                                                                  |
| `items.meta.spell.hunspell_language_code` | string  | **Spellcheck language code**.                                                                                                                                                                                                                                  |
| `items.meta.spell.misspelled`  | array   | **Array of misspelled words**.                                                                                                                                                                                                                                   |
| `items.meta.spell.misspelled.word` | string  | **Misspelled word**.                                                                                                                                                                                                                                               |
| `items.meta.social_media_tags` | object  | **Object of social media tags** found on the page, containing tags and their content (e.g., Open Graph and Twitter card tags like `og:locale`, `og:type`, `twitter:card`, etc.).                                                                         |
| `page_timing`                  | object  | **Object of page load metrics**.                                                                                                                                                                                                                               |
| `page_timing.time_to_interactive` | integer | **Time To Interactive (TTI) metric**. The time until the user can interact with a page (in milliseconds).                                                                                                                                                      |
| `page_timing.dom_complete`     | integer | **Time to load resources**. The time until the page and all of its subresources are downloaded (in milliseconds).                                                                                                                                              |
| `page_timing.largest_contentful_paint` | float | **Core Web Vitals metric measuring how fast the largest above-the-fold content element is displayed** (in milliseconds).                                                                                                                                   |
| `page_timing.first_input_delay` | float   | **Core Web Vitals metric indicating the responsiveness of a page**. Time from user interaction to browser response (in milliseconds).                                                                                                                           |
| `page_timing.connection_time`  | integer | **Time to connect to a server** (in milliseconds).                                                                                                                                                                                                             |
| `page_timing.time_to_secure_connection` | integer | **Time to establish a secure connection** (in milliseconds).                                                                                                                                                                                                 |
| `page_timing.request_sent_time` | integer | **Time to send a request to a server** (in milliseconds).                                                                                                                                                                                                      |
| `page_timing.waiting_time`     | integer | **Time to first byte (TTFB)** in milliseconds.                                                                                                                                                                                                                 |
| `page_timing.download_time`    | integer | **Time it takes for a browser to receive a response** (in milliseconds).                                                                                                                                                                                       |
| `page_timing.duration_time`    | integer | **Total time it takes until a browser receives a complete response from a server** (in milliseconds).                                                                                                                                                          |
| `page_timing.fetch_start`      | integer | **Time to start downloading the HTML resource**. The amount of time the browser needs to start downloading a page.                                                                                                                                               |
| `page_timing.fetch_end`        | integer | **Time to complete downloading the HTML resource**. The amount of time the browser needs to complete downloading a page.                                                                                                                                           |
| `onpage_score`                 | float   | **Shows how page is optimized on a 100-point scale**. 100 is the highest possible score.                                                                                                                                                                       |
| `total_dom_size`               | integer | **Total DOM size of a page**.                                                                                                                                                                                                                                  |
| `custom_js_response`           | string/object/integer | **The result of executing a specified JS script**. The field type and value depend on the script specified in the `custom_js` field. Results can be filtered by this value.                                                                 |
| `custom_js_client_exception`   | string  | **Error when executing a custom JS**. If an error occurred, the error message will be displayed here.                                                                                                                                                          |
| `resource_errors`              | object  | **Resource errors and warnings**.                                                                                                                                                                                                                              |
| `resource_errors.errors`       | array   | **Resource errors**.                                                                                                                                                                                                                                           |
| `resource_errors.errors.line`  | integer | **Line where the error was found**.                                                                                                                                                                                                                            |
| `resource_errors.errors.column` | integer | **Column where the error was found**.                                                                                                                                                                                                                          |
| `resource_errors.errors.message` | string  | **Text message of the error**. Possible HTML errors are available.                                                                                                                                                                                      |
| `resource_errors.errors.status_code` | integer | **Status code of the error**. Possible values: `0` (Unidentified), `501` (Html Parse Error), `1501` (JS Parse Error), `2501` (CSS Parse Error), `3501` (Image Parse Error), `3502` (Image Scale Is Zero), `3503` (Image Size Is Zero), `3504` (Image Format Invalid). |
| `resource_errors.warnings`     | array   | **Resource warnings**.                                                                                                                                                                                                                                         |
| `resource_errors.warnings.line` | integer | **Line the warning relates to**. `0` means the warning relates to the whole page.                                                                                                                                                                             |
| `resource_errors.warnings.column` | integer | **Column the warning relates to**. `0` means the warning relates to the whole page.                                                                                                                                                                           |
| `resource_errors.warnings.message` | string  | **Text message of the warning**. Possible messages: "Has node with more than 60 childs.", "Has more that 1500 nodes.", "HTML depth more than 32 tags.".                                                                                                    |
| `resource_errors.warnings.status_code` | integer | **Status code of the warning**. Possible values: `0` (Unidentified), `1` (Has node with more than 60 childs), `2` (Has more that 1500 nodes), `3` (HTML depth more than 32 tags).                                                                     |
| `broken_resources`             | boolean | **Indicates whether a page contains broken resources**.                                                                                                                                                                                                        |
| `broken_links`                 | boolean | **Indicates whether a page contains broken links**.                                                                                                                                                                                                            |
| `duplicate_title`              | boolean | **Indicates whether a page has duplicate `title` tags**.                                                                                                                                                                                                       |
| `duplicate_description`        | boolean | **Indicates whether a page has a duplicate description**.                                                                                                                                                                                                      |
| `duplicate_content`            | boolean | **Indicates whether a page has duplicate content**.                                                                                                                                                                                                            |
| `click_depth`                  | integer | **Number of clicks it takes to get to the page** from the homepage.                                                                                                                                                                                            |
| `size`                         | integer | **Resource size** in bytes.                                                                                                                                                                                                                                    |
| `encoded_size`                 | integer | **Page size after encoding** in bytes.                                                                                                                                                                                                                         |
| `total_transfer_size`          | integer | **Compressed page size** in bytes.                                                                                                                                                                                                                             |
| `fetch_time`                   | string  | **Date and time when a resource was fetched** in UTC format: “yyyy-mm-dd hh-mm-ss +00:00”.                                                                                                                                                              |
| `cache_control`                | object  | **Instructions for caching**.                                                                                                                                                                                                                                  |
| `cache_control.cachable`       | boolean | **Indicates whether the page is cacheable**.                                                                                                                                                                                                                   |
| `cache_control.ttl`            | integer | **Time to live**. The amount of time the browser caches a resource.                                                                                                                                                                                            |
| `checks`                       | object  | **Website checks** related to the page.                                                                                                                                                                                                                        |
| `checks.no_content_encoding`   | boolean | **Page with no content encoding**. Indicates whether a page has no compression algorithm of the content.                                                                                                                                                       |
| `checks.high_loading_time`     | boolean | **Page with high loading time**. Indicates whether a page loading time exceeds 3 seconds.                                                                                                                                                                      |
| `checks.is_redirect`           | boolean | **Page with redirects**. Indicates whether a page has `3XX` redirects to other pages.                                                                                                                                                                          |
| `checks.is_4xx_code`           | boolean | **Page with `4xx` status codes**. Indicates whether a page has a `4xx` response code.                                                                                                                                                                        |
| `checks.is_5xx_code`           | boolean | **Page with `5xx` status codes**. Indicates whether a page has a `5xx` response code.                                                                                                                                                                        |
| `checks.is_broken`             | boolean | **Broken page**. Indicates whether a page returns a response code less than `200` or greater than `400`.                                                                                                                                                   |
| `checks.is_www`                | boolean | **Page with www**. Indicates whether a page is on a `www` subdomain.                                                                                                                                                                                           |
| `checks.is_https`              | boolean | **Page with the https protocol**.                                                                                                                                                                                                                              |
| `checks.is_http`               | boolean | **Page with the http protocol**.                                                                                                                                                                                                                               |
| `checks.high_waiting_time`     | boolean | **Page with high waiting time**. Indicates whether a page waiting time (Time to First Byte) exceeds 1.5 seconds.                                                                                                                                              |
| `checks.has_micromarkup`       | boolean | **Page contains microdata markup**.                                                                                                                                                                                                                                |
| `checks.has_micromarkup_errors` | boolean | **Page contains microdata markup errors**.                                                                                                                                                                                                                         |
| `checks.no_doctype`            | boolean | **Page with no doctype**. Indicates whether a page is without the `<!DOCTYPE HTML>` declaration.                                                                                                                                                            |
| `checks.has_html_doctype`      | boolean | **Page with HTML doctype declaration**. `true` if the page has HTML `DOCTYPE` declaration.                                                                                                                                                                   |
| `checks.canonical`             | boolean | **Page is canonical**.                                                                                                                                                                                                                                         |
| `checks.no_encoding_meta_tag`  | boolean | **Page with no meta tag encoding**. Indicates whether a page is without `Content-Type`. Available for pages with `canonical` check set to `true`.                                                                                                       |
| `checks.no_h1_tag`             | boolean | **Page with empty or absent h1 tags**. Available for pages with `canonical` check set to `true`.                                                                                                                                                            |
| `checks.https_to_http_links`   | boolean | **HTTPS page has links to HTTP pages**. `true` if this HTTPS page has links to HTTP pages. Available for pages with `canonical` check set to `true`.                                                                                                        |
| `checks.size_greater_than_3mb` | boolean | **Page with size larger than 3 MB**. `true` if the page size is exceeding 3 MB. Available for pages with `canonical` check set to `true`.                                                                                                                   |
| `checks.meta_charset_consistency` | boolean | **Consistency between charset encoding and page charset**. `true` if the page’s charset encoding doesn’t match the actual charset of the page. Available for pages with `canonical` check set to `true`.                                                      |
| `checks.has_meta_refresh_redirect` | boolean | **Pages with meta refresh redirect**. `true` if the page has `<meta http-equiv=”refresh”>` tag. Available for pages with `canonical` check set to `true`.                                                                                                 |
| `checks.has_render_blocking_resources` | boolean | **Page with render-blocking resources**. `true` if the page has render-blocking scripts or stylesheets. Available for pages with `canonical` check set to `true`.                                                                                      |
| `checks.low_content_rate`      | boolean | **Page with low content rate**. Indicates whether a page has the `plaintext size` to `page size` ratio of less than 0.1. Available for pages with `canonical` check set to `true`.                                                                            |
| `checks.high_content_rate`     | boolean | **Page with high content rate**. Indicates whether a page has the `plaintext size` to `page size` ratio of more than 0.9. Available for pages with `canonical` check set to `true`.                                                                           |
| `checks.low_character_count`   | boolean | **Indicates whether the page has less than 1024 characters**. Available for pages with `canonical` check set to `true`.                                                                                                                                      |
| `checks.high_character_count`  | boolean | **Indicates whether the page has more than 256,000 characters**. Available for pages with `canonical` check set to `true`.                                                                                                                                     |
| `checks.small_page_size`       | boolean | **Indicates whether a page is too small**. `true` if a page size is smaller than 1024 bytes. Available for pages with `canonical` check set to `true`.                                                                                                       |
| `checks.large_page_size`       | boolean | **Indicates whether a page is too heavy**. `true` if a page size exceeds 1 megabyte. Available for pages with `canonical` check set to `true`.                                                                                                               |
| `checks.low_readability_rate`  | boolean | **Page with a low readability rate**. Indicates whether a page is scored less than 15 points on the Flesch–Kincaid readability test. Available for pages with `canonical` check set to `true`.                                                                |
| `checks.irrelevant_description` | boolean | **Page with irrelevant description**. Indicates whether a page `description` tag is irrelevant to the content of a page (relevance threshold is 0.2). Available for pages with `canonical` check set to `true`.                                                 |
| `checks.irrelevant_title`      | boolean | **Page with irrelevant title**. Indicates whether a page `title` tag is irrelevant to the content of the page (relevance threshold is 0.3). Available for pages with `canonical` check set to `true`.                                                         |
| `checks.irrelevant_meta_keywords` | boolean | **Page with irrelevant meta keywords**. Indicates whether a page `keywords` tags are irrelevant to the content of a page (relevance threshold is 0.6). Available for pages with `canonical` check set to `true`.                                              |
| `checks.title_too_long`        | boolean | **Page with a long title**. Indicates whether the content of the `title` tag exceeds 65 characters. Available for pages with `canonical` check set to `true`.                                                                                                 |
| `checks.has_meta_title`        | boolean | **Page has a meta title**. Indicates whether the HTML of a page contains the `meta_title` tag. Available for pages with `canonical` check set to `true`.                                                                                                   |
| `checks.title_too_short`       | boolean | **Page with short titles**. Indicates whether the content of `title` tag is shorter than 30 characters. Available for pages with `canonical` check set to `true`.                                                                                             |
| `checks.deprecated_html_tags`  | boolean | **Page with deprecated tags**. Indicates whether a page has deprecated HTML tags. Available for pages with `canonical` check set to `true`.                                                                                                                 |
| `checks.duplicate_meta_tags`   | boolean | **Page with duplicate meta tags**. Indicates whether a page has more than one meta tag of the same type. Available for pages with `canonical` check set to `true`.                                                                                          |
| `checks.duplicate_title_tag`   | boolean | **Page with more than one title tag**. Indicates whether a page has more than one `title` tag. Available for pages with `canonical` check set to `true`.                                                                                                    |
| `checks.no_image_alt`          | boolean | **Images without `alt` tags**. Available for pages with `canonical` check set to `true`.                                                                                                                                                                     |
| `checks.no_image_title`        | boolean | **Images without `title` tags**. Available for pages with `canonical` check set to `true`.                                                                                                                                                                   |
| `checks.no_description`        | boolean | **Pages with no description**. Indicates whether a page has an empty or absent `description` meta tag. Available for pages with `canonical` check set to `true`.                                                                                             |
| `checks.no_title`              | boolean | **Page with no title**. Indicates whether a page has an empty or absent `title` tag. Available for pages with `canonical` check set to `true`.                                                                                                             |
| `checks.no_favicon`            | boolean | **Page with no favicon**. Available for pages with `canonical` check set to `true`.                                                                                                                                                                          |
| `checks.seo_friendly_url`      | boolean | **Page with seo-friendly URL**. Checked by four parameters: relative path length < 120 chars, no special characters, no dynamic parameters, URL relevance to the page. If any fail, URL is not SEO-friendly. Available for pages with `canonical` check set to `true`. |
| `checks.flash`                 | boolean | **Page with flash**. Indicates whether a page has flash elements.                                                                                                                                                                                              |
| `checks.frame`                 | boolean | **Page with frames**. Indicates whether a page contains `frame`, `iframe`, `frameset` tags.                                                                                                                                                                  |
| `checks.lorem_ipsum`           | boolean | **Page with lorem ipsum**. Indicates whether a page has *lorem ipsum* content. Available for pages with `canonical` check set to `true`.                                                                                                                 |
| `checks.has_misspelling`       | boolean | **Page with misspelling**. Indicates whether a page has spelling mistakes. Informative if `check_spell` was set to `true` in the POST array.                                                                                                                  |
| `checks.seo_friendly_url_characters_check` | boolean | **URL characters check-up**. Indicates whether a page URL contains only uppercase/lowercase Latin characters, digits, and dashes.                                                                                                                  |
| `checks.seo_friendly_url_dynamic_check` | boolean | **URL dynamic check-up**. `true` if a page has no dynamic parameters in the URL.                                                                                                                                                                     |
| `checks.seo_friendly_url_keywords_check` | boolean | **URL keyword check-up**. Indicates whether a page URL is consistent with the `title` meta tag.                                                                                                                                                  |
| `checks.seo_friendly_url_relative_length_check` | boolean | **URL length check-up**. `true` if a page URL is no longer than 120 characters.                                                                                                                                                              |
| `content_encoding`             | string  | **Type of encoding** (e.g., "br").                                                                                                                                                                                                                             |
| `media_type`                   | string  | **Types of media** used to display a page (e.g., "text/html").                                                                                                                                                                                                 |
| `server`                       | string  | **Server version** (e.g., "cloudflare").                                                                                                                                                                                                                       |
| `is_resource`                  | boolean | **Indicates whether a page is a single resource**.                                                                                                                                                                                                             |
| `url_length`                   | integer | **Page URL length** in characters.                                                                                                                                                                                                                                 |
| `relative_url_length`          | integer | **Relative URL length** in characters.                                                                                                                                                                                                                             |
| `last_modified`                | object  | **Contains data on changes related to the resource**. `null` if no data.                                                                                                                                                                                       |
| `last_modified.header`         | string  | **Date and time when the header was last modified** in UTC format. `null` if no data.                                                                                                                                                                     |
| `last_modified.sitemap`        | string  | **Date and time when the sitemap was last modified** in UTC format. `null` if no data.                                                                                                                                                                    |
| `last_modified.meta_tag`       | string  | **Date and time when the meta tag was last modified** in UTC format. `null` if no data.                                                                                                                                                                   |

---

#### **`resource_type`: 'broken' (for broken pages)**

| Field Name                   | Type    | Description                                                                                                                                                                                  |
| :--------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_type`              | string  | Type of the returned resource. Equals `'broken'`.                                                                                                                                       |
| `status_code`                | integer | **Status code of the page**.                                                                                                                                                            |
| `location`                   | string  | **Location header**. Indicates the URL to redirect a page to.                                                                                                                           |
| `url`                        | string  | **Page URL**.                                                                                                                                                                           |
| `size`                       | integer | **Resource size** in bytes.                                                                                                                                                             |
| `encoded_size`               | integer | **Page size after encoding** in bytes.                                                                                                                                                  |
| `total_transfer_size`        | integer | **Compressed page size** in bytes.                                                                                                                                                      |
| `fetch_time`                 | string  | **Date and time when a resource was fetched** in UTC format.                                                                                                                            |
| `fetch_timing`               | object  | **Time range within which a result was fetched**.                                                                                                                                       |
| `fetch_timing.duration_time` | integer | **Indicates how many seconds it took to download a page**.                                                                                                                              |
| `fetch_timing.fetch_start`   | integer | **Time to start downloading the HTML resource**.                                                                                                                                        |
| `fetch_timing.fetch_end`     | integer | **Time to complete downloading the HTML resource**.                                                                                                                                     |
| `cache_control`              | object  | **Instructions for caching**.                                                                                                                                                           |
| `cache_control.cachable`     | boolean | **Indicates whether the page is cacheable**.                                                                                                                                            |
| `cache_control.ttl`          | integer | **Time to live**. The amount of time the browser caches a resource.                                                                                                                     |
| `checks`                     | object  | **On-page check-ups**.                                                                                                                                                                  |
| `checks.no_content_encoding` | boolean | **Page with no content encoding**.                                                                                                                                                      |
| `checks.high_loading_time`   | boolean | **Page with high loading time**.                                                                                                                                                        |
| `checks.is_redirect`         | boolean | **Page with redirects**.                                                                                                                                                                |
| `checks.is_4xx_code`         | boolean | **Page with `4xx` status codes**.                                                                                                                                                       |
| `checks.is_5xx_code`         | boolean | **Page with `5xx` status codes**.                                                                                                                                                       |
| `checks.is_broken`           | boolean | **Broken page**.                                                                                                                                                                        |
| `checks.is_www`              | boolean | **Page with www**.                                                                                                                                                                      |
| `checks.is_https`            | boolean | **Page with the https protocol**.                                                                                                                                                       |
| `checks.is_http`             | boolean | **Page with the http protocol**.                                                                                                                                                        |
| `resource_errors`            | object  | **Resource errors and warnings**. (Same sub-fields as for 'html' resource type: `errors`, `errors.line`, `errors.column`, `errors.message`, `errors.status_code`, `warnings`, `warnings.line`, `warnings.column`, `warnings.message`, `warnings.status_code`). |
| `content_encoding`           | string  | **Type of encoding**.                                                                                                                                                                   |
| `media_type`                 | string  | **Types of media** used to display a page (e.g., "text/html").                                                                                                                          |
| `server`                     | string  | **Server version**.                                                                                                                                                                     |
| `is_resource`                | boolean | **Indicates whether a page is a single resource**.                                                                                                                                      |
| `last_modified`              | object  | **Contains data on changes related to the resource**. `null` if no data. (Same sub-fields as for 'html' resource type: `header`, `sitemap`, `meta_tag`).                           |

---

#### **`resource_type`: 'redirect' (for redirect pages)**

| Field Name                   | Type    | Description                                                                                                                                                                                  |
| :--------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_type`              | string  | Type of the returned resource. Equals `'redirect'`.                                                                                                                                     |
| `status_code`                | integer | **Status code of the page**.                                                                                                                                                            |
| `location`                   | string  | **Target URL** for "redirect" resources.                                                                                                                                                |
| `url`                        | string  | **Source URL** for "redirect" resources.                                                                                                                                                |
| `size`                       | integer | **Resource size** in bytes. Equals `0` for "redirect" resources.                                                                                                                        |
| `encoded_size`               | integer | **Page size after encoding**. Equals `0` for "redirect" resources.                                                                                                                      |
| `total_transfer_size`        | integer | **Compressed page size** in bytes.                                                                                                                                                      |
| `fetch_time`                 | string  | **Date and time when a resource was fetched** in UTC format.                                                                                                                            |
| `fetch_timing`               | object  | **Time range within which a result was fetched**.                                                                                                                                       |
| `fetch_timing.duration_time` | integer | **Indicates how many seconds it took to download a page**.                                                                                                                              |
| `fetch_timing.fetch_start`   | integer | **Time to start downloading the HTML resource**.                                                                                                                                        |
| `fetch_timing.fetch_end`     | integer | **Time to complete downloading the HTML resource**.                                                                                                                                     |
| `resource_errors`            | object  | **Resource errors and warnings**. (Same sub-fields as for 'html' resource type: `errors`, `errors.line`, `errors.column`, `errors.message`, `errors.status_code`, `warnings`, `warnings.line`, `warnings.column`, `warnings.message`, `warnings.status_code`). |
| `cache_control`              | object  | **Instructions for caching**. (Same sub-fields as for 'html' resource type: `cachable`, `ttl`).                                                                                   |
| `checks`                     | object  | **On-page check-ups**. (Same sub-fields as for 'html' resource type regarding loading/status codes/protocols: `no_content_encoding`, `high_loading_time`, `is_redirect`, `is_4xx_code`, `is_5xx_code`, `is_broken`, `is_www`, `is_https`, `is_http`). |
| `content_encoding`           | string  | **Type of encoding**.                                                                                                                                                                   |
| `media_type`                 | string  | **Types of media** used to display a page (e.g., "text/html").                                                                                                                          |
| `server`                     | string  | **Server version**.                                                                                                                                                                     |
| `is_resource`                | boolean | **Indicates whether a page is a single resource**.                                                                                                                                      |
| `last_modified`              | object  | **Contains data on changes related to the resource**. `null` if no data. (Same sub-fields as for 'html' resource type: `header`, `sitemap`, `meta_tag`).                           |

---

#### **`resource_type`: 'script', 'image', 'stylesheet' (for resources)**
(Note: These types of resources are displayed only if the first URL to crawl is a script, image, or stylesheet.)

| Field Name                   | Type    | Description                                                                                                                                                                                  |
| :--------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_type`              | string  | **Type of the returned resource**. Possible types: `script`, `image`, `stylesheet`.                                                                                                     |
| `meta`                       | object  | **Resource properties**. Available only for items with `resource_type: 'image'`.                                                                                                        |
| `meta.alternative_text`      | string  | **Content of the image `alt` attribute**.                                                                                                                                               |
| `meta.title`                 | string  | **Title**.                                                                                                                                                                              |
| `meta.original_width`        | integer | **Original image width** in px.                                                                                                                                                         |
| `meta.original_height`       | integer | **Original image height** in px.                                                                                                                                                        |
| `meta.width`                 | integer | **Image width** in px.                                                                                                                                                                  |
| `meta.height`                | integer | **Image height** in px.                                                                                                                                                                 |
| `status_code`                | integer | **Status code of the page** where a given resource is located.                                                                                                                          |
| `location`                   | string  | **Location header**. Indicates the URL to redirect a page to.                                                                                                                           |
| `url`                        | string  | **Resource URL**.                                                                                                                                                                       |
| `size`                       | integer | **Resource size** in bytes.                                                                                                                                                             |
| `encoded_size`               | integer | **Resource size after encoding** in bytes.                                                                                                                                              |
| `total_transfer_size`        | integer | **Compressed resource size** in bytes.                                                                                                                                                  |
| `fetch_time`                 | string  | **Date and time when a resource was fetched** in UTC format.                                                                                                                            |
| `fetch_timing`               | object  | **Resource fetching time range**.                                                                                                                                                       |
| `fetch_timing.duration_time` | integer | **Indicates how many milliseconds it took to fetch a resource**.                                                                                                                        |
| `fetch_timing.fetch_start`   | integer | **Time to start downloading the resource**.                                                                                                                                             |
| `fetch_timing.fetch_end`     | integer | **Time to complete downloading the resource**.                                                                                                                                          |
| `cache_control`              | object  | **Instructions for caching**. (Same sub-fields as for 'html' resource type: `cachable`, `ttl`).                                                                                   |
| `checks`                     | object  | **Resource check-ups**. Contents depend on the `resource_type`.                                                                                                                         |
| `checks.no_content_encoding` | boolean | **Resource with no content encoding**.                                                                                                                                                  |
| `checks.high_loading_time`   | boolean | **Resource with high loading time**.                                                                                                                                                    |
| `checks.is_redirect`         | boolean | **Resource with redirects**.                                                                                                                                                            |
| `checks.is_4xx_code`         | boolean | **Resource with `4xx` status codes**.                                                                                                                                                   |
| `checks.is_5xx_code`         | boolean | **Resource with `5xx` status codes**.                                                                                                                                                   |
| `checks.is_broken`           | boolean | **Broken resource**.                                                                                                                                                                    |
| `checks.is_www`              | boolean | **Page with www**.                                                                                                                                                                      |
| `checks.is_https`            | boolean | **Page with the https protocol**.                                                                                                                                                       |
| `checks.is_http`             | boolean | **Page with the http protocol**.                                                                                                                                                        |
| `checks.is_minified`         | boolean | **Resource is minified**. Indicates whether the content of a stylesheet or script is minified. Available for `stylesheet`, `script`.                                                      |
| `checks.has_redirect`        | boolean | **Resource has a redirect**. Available for `script`, `image`. Indicates redirects pointing at the resource or if the script contains a redirect.                                        |
| `checks.has_subrequests`     | boolean | **Resource contains subrequests**. Indicates whether the content of a stylesheet or script contain additional requests. Available for `stylesheet`, `script`.                           |
| `checks.original_size_displayed` | boolean | **Image displayed in its original size**. Available only for `image`.                                                                                                                   |
| `resource_errors`            | object  | **Resource errors and warnings**. (Same sub-fields as for 'html' resource type: `errors`, `errors.line`, `errors.column`, `errors.message`, `errors.status_code`, `warnings`, `warnings.line`, `warnings.column`, `warnings.message`, `warnings.status_code`). |
| `content_encoding`           | string  | **Type of encoding**.                                                                                                                                                                   |
| `media_type`                 | string  | **Types of media** used to display a resource.                                                                                                                                          |
| `accept_type`                | string  | **Indicates the expected type of resource**. For a broken resource, indicates its original type. Possible values: `any`, `none`, `image`, `sitemap`, `robots`, `script`, `stylesheet`, `redirect`, `html`, `text`, `other`, `font`. |
| `server`                     | string  | **Server version**.                                                                                                                                                                     |
| `last_modified`              | object  | **Contains data on changes related to the resource**. `null` if no data. (Same sub-fields as for 'html' resource type: `header`, `sitemap`, `meta_tag`).                           |

--- 

Based on the sources provided, this documentation covers two distinct endpoints within the DataForSEO Labs API: `dataforseo_labs/google/keyword_ideas/live` and `dataforseo_labs/google/serp_competitors/live`.

***
