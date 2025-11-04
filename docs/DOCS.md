## Keyword Ideas

‌

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


**`POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live`**

Your account will be charged for each request.

The cost can be calculated on the [Pricing](https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api "Pricing") page.

All POST data should be sent in the [JSON](https://en.wikipedia.org/wiki/JSON) format (UTF-8 encoding). The task setting is done using the POST method. When setting a task, you should send all task parameters in the task array of the generic POST array. You can send up to 2000 API calls per minute. The maximum number of requests that can be sent simultaneously is limited to 30.

You can specify the number of results you want to retrieve and sort them.

Below you will find a detailed description of the fields you can use for setting a task.


**Code**

{
  "version": "0.1.20240801",
  "status_code": 20000,
  "status_message": "Ok.",
  "time": "0.7097 sec.",
  "cost": 0.0103,
  "tasks_count": 1,
  "tasks_error": 0,
  "tasks": [
    {
      "id": "08221822-1535-0400-0000-8fccf5eb0f23",
      "status_code": 20000,
      "status_message": "Ok.",
      "time": "0.6455 sec.",
      "cost": 0.0103,
      "result_count": 1,
      "path": [
        "v3",
        "dataforseo_labs",
        "google",
        "keyword_ideas",
        "live"
      ],
      "data": {
        "api": "dataforseo_labs",
        "function": "keyword_ideas",
        "se_type": "google",
        "keywords": [
          "phone",
          "watch"
        ],
        "location_code": 2840,
        "language_code": "en",
        "include_serp_info": true,
        "limit": 3
      },
      "result": [
        {
          "se_type": "google",
          "seed_keywords": [
            "phone",
            "watch"
          ],
          "location_code": 2840,
          "language_code": "en",
          "total_count": 533763,
          "items_count": 3,
          "offset": 0,
          "offset_token": "eyJDdXJyZW50T2Zmc2V0IjozLCJSZXF1ZXN0RGF0YSI6eyJrZXl3b3JkcyI6WyJwaG9uZSIsIndhdGNoIl0sImxvY2F0aW9uIjoyODQwLCJsYW5ndWFnZSI6ImVuIiwiY2xvc2VseV92YXJpYW50cyI6ZmFsc2UsIm5ld2VzdCI6ZmFsc2UsImV4dGVuZGVkIjpmYWxzZSwibG9hZF9zZXJwX2luZm8iOnRydWUsImF1dG9jb3JyZWN0Ijp0cnVlLCJJc09sZCI6ZmFsc2UsInNlYXJjaF9hZnRlcl90b2tlbiI6bnVsbCwiaWdub3JlX3N5bm9ueW1zIjpmYWxzZSwic2VhcmNoX2VuZ2luZSI6Imdvb2dsZSIsInVzZV9uZXdfY2F0ZWdvcmllcyI6dHJ1ZSwib3JkZXJfYnkiOnsib3JkZXJfZmllbGQiOiJfc2NvcmUiLCJvcmRlcl90eXBlIjoiRGVzYyIsIm5leHQiOm51bGx9LCJsaW1pdCI6Mywib2Zmc2V0IjowLCJhaWQiOjE1MzV9LCJSYXdRdWVyeSI6bnVsbCwiSWQiOiJiNWEyZGNlOS00Mzk3LTQ3NTgtYWEyOC02NWFiMzY3ZDM5NDgiLCJTZWFyY2hBZnRlckRhdGEiOlszMDQuMTc2NTcsImUwNGZkMDE1LTllY2YtMzcwYi0xZGJmLWY0NGExODVjOWU5ZiJdfQ==",
          "items": [
            {
              "se_type": "google",
              "keyword": "phone",
              "location_code": 2840,
              "language_code": "en",
              "keyword_info": {
                "se_type": "google",
                "last_updated_time": "2024-08-11 13:24:34 +00:00",
                "competition": 1,
                "competition_level": "HIGH",
                "cpc": 5.98,
                "search_volume": 368000,
                "low_top_of_page_bid": 3.08,
                "high_top_of_page_bid": 10.5,
                "categories": [
                  10007,
                  10878,
                  12133,
                  13381
                ],
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 450000
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 368000
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 368000
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 368000
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 368000
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 368000
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 368000
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 368000
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 368000
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 368000
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 368000
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 368000
                  }
                ],                
                "search_volume_trend": {
                  "monthly": 22,
                  "quarterly": 22,
                  "yearly": 0
                }
              },
              "clickstream_keyword_info": null,
              "keyword_properties": {
                "se_type": "google",
                "core_keyword": null,
                "synonym_clustering_algorithm": "text_processing",
                "keyword_difficulty": 83,
                "detected_language": "en",
                "is_another_language": false
              },
              "serp_info": {
                "se_type": "google",
                "check_url": "https://www.google.com/search?q=phone&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",
                "serp_item_types": [
                  "popular_products",
                  "images",
                  "organic",
                  "product_considerations",
                  "refine_products",
                  "top_stories",
                  "related_searches"
                ],
                "se_results_count": 19880000000,
                "last_updated_time": "2024-07-14 21:43:34 +00:00",
                "previous_updated_time": "2024-05-18 19:29:28 +00:00"
              },
              "avg_backlinks_info": {
                "se_type": "google",
                "backlinks": 6835.7,
                "dofollow": 3775.6,
                "referring_pages": 5352.2,
                "referring_domains": 1100.3,
                "referring_main_domains": 955.1,
                "rank": 369.3,
                "main_domain_rank": 681.2,
                "last_updated_time": "2024-07-14 21:43:39 +00:00"
              },
              "search_intent_info": {
                "se_type": "google",
                "main_intent": "navigational",
                "foreign_intent": [
                  "commercial"
                ],
                "last_updated_time": "2023-03-02 03:55:21 +00:00"
              },
              "keyword_info_normalized_with_bing": {
                "last_updated_time": "2024-08-17 01:41:37 +00:00",
                "search_volume": 308309,
                "is_normalized": true,
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 377009
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 308309
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 308309
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 308309
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 308309
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 308309
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 308309
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 308309
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 308309
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 308309
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 308309
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 308309
                  },
                  {
                    "year": 2023,
                    "month": 7,
                    "search_volume": 300631
                  }
                ]
              },
              "keyword_info_normalized_with_clickstream": {
                "last_updated_time": "2024-08-17 01:41:37 +00:00",
                "search_volume": 324416,
                "is_normalized": true,
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 396705
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 324416
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 324416
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 324416
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 324416
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 324416
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 324416
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 324416
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 324416
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 324416
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 324416
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 324416
                  },
                  {
                    "year": 2023,
                    "month": 7,
                    "search_volume": 324365
                  }
                ]
              }
            },
            {
              "se_type": "google",
              "keyword": "cell phone signal booster",
              "location_code": 2840,
              "language_code": "en",
              "keyword_info": {
                "se_type": "google",
                "last_updated_time": "2024-08-11 18:11:54 +00:00",
                "competition": 1,
                "competition_level": "HIGH",
                "cpc": 1.05,
                "search_volume": 22200,
                "low_top_of_page_bid": 0.31,
                "high_top_of_page_bid": 1.15,
                "categories": [
                  10007,
                  10878,
                  12133,
                  13381
                ],
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 33100
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 27100
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 22200
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 18100
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 18100
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 18100
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 18100
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 22200
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 22200
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 27100
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 27100
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 27100
                  }
                ],
                "search_volume_trend": {
                  "monthly": 22,
                  "quarterly": 22,
                  "yearly": 0
                }
              },
              "clickstream_keyword_info": null,
              "keyword_properties": {
                "se_type": "google",
                "core_keyword": "cell phone signal booster for phone",
                "synonym_clustering_algorithm": "text_processing",
                "keyword_difficulty": 23,
                "detected_language": "en",
                "is_another_language": false
              },
              "serp_info": {
                "se_type": "google",
                "check_url": "https://www.google.com/search?q=cell%20phone%20signal%20booster&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",
                "serp_item_types": [
                  "popular_products",
                  "people_also_ask",
                  "organic",
                  "images",
                  "related_searches"
                ],
                "se_results_count": 13500000,
                "last_updated_time": "2024-08-04 11:06:04 +00:00",
                "previous_updated_time": "2024-06-22 20:35:21 +00:00"
              },
              "avg_backlinks_info": {
                "se_type": "google",
                "backlinks": 111.6,
                "dofollow": 34.7,
                "referring_pages": 104.5,
                "referring_domains": 29,
                "referring_main_domains": 26.3,
                "rank": 103.5,
                "main_domain_rank": 530.7,
                "last_updated_time": "2024-08-04 11:06:06 +00:00"
              },
              "search_intent_info": {
                "se_type": "google",
                "main_intent": "transactional",
                "foreign_intent": null,
                "last_updated_time": "2023-03-03 12:40:39 +00:00"
              },
              "keyword_info_normalized_with_bing": {
                "last_updated_time": "2024-08-16 10:43:48 +00:00",
                "search_volume": 12895,
                "is_normalized": true,
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 19226
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 15741
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 12895
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 10513
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 10513
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 10513
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 10513
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 12895
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 12895
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 15741
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 15741
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 15741
                  },
                  {
                    "year": 2023,
                    "month": 7,
                    "search_volume": 19139
                  }
                ]
              },
              "keyword_info_normalized_with_clickstream": {
                "last_updated_time": "2024-08-16 10:43:48 +00:00",
                "search_volume": 15498,
                "is_normalized": true,
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 23107
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 18918
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 15498
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 12635
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 12635
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 12635
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 12635
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 15498
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 15498
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 18918
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 18918
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 18918
                  },
                  {
                    "year": 2023,
                    "month": 7,
                    "search_volume": 22930
                  }
                ]
              }
            },
            {
              "se_type": "google",
              "keyword": "phone charm",
              "location_code": 2840,
              "language_code": "en",
              "keyword_info": {
                "se_type": "google",
                "last_updated_time": "2024-08-12 16:45:18 +00:00",
                "competition": 1,
                "competition_level": "HIGH",
                "cpc": 0.66,
                "search_volume": 27100,
                "low_top_of_page_bid": 0.26,
                "high_top_of_page_bid": 1.93,
                "categories": [
                  10007,
                  10878,
                  12133,
                  13381
                ],
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 33100
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 27100
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 27100
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 22200
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 27100
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 22200
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 27100
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 27100
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 27100
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 22200
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 22200
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 27100
                  }
                ],                
                "search_volume_trend": {
                  "monthly": 22,
                  "quarterly": 22,
                  "yearly": 0
                }
              },
              "clickstream_keyword_info": null,
              "keyword_properties": {
                "se_type": "google",
                "core_keyword": "charms for phones",
                "synonym_clustering_algorithm": "text_processing",
                "keyword_difficulty": 0,
                "detected_language": "en",
                "is_another_language": false
              },
              "serp_info": {
                "se_type": "google",
                "check_url": "https://www.google.com/search?q=phone%20charm&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",
                "serp_item_types": [
                  "popular_products",
                  "organic",
                  "people_also_ask",
                  "images",
                  "explore_brands",
                  "related_searches"
                ],
                "se_results_count": 284000000,
                "last_updated_time": "2024-08-04 10:21:18 +00:00",
                "previous_updated_time": "2024-06-22 19:50:30 +00:00"
              },
              "avg_backlinks_info": {
                "se_type": "google",
                "backlinks": 15.9,
                "dofollow": 9,
                "referring_pages": 10.5,
                "referring_domains": 3,
                "referring_main_domains": 2.6,
                "rank": 44.1,
                "main_domain_rank": 491.8,
                "last_updated_time": "2024-08-04 10:21:19 +00:00"
              },
              "search_intent_info": {
                "se_type": "google",
                "main_intent": "transactional",
                "foreign_intent": null,
                "last_updated_time": "2023-03-02 03:55:42 +00:00"
              },
              "keyword_info_normalized_with_bing": {
                "last_updated_time": "2024-08-17 03:47:30 +00:00",
                "search_volume": 14892,
                "is_normalized": true,
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 18190
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 14892
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 14892
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 12200
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 14892
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 12200
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 14892
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 14892
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 14892
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 12200
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 12200
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 14892
                  },
                  {
                    "year": 2023,
                    "month": 7,
                    "search_volume": 15028
                  }
                ]
              },
              "keyword_info_normalized_with_clickstream": {
                "last_updated_time": "2024-08-17 03:47:30 +00:00",
                "search_volume": 13826,
                "is_normalized": true,
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 16887
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 13826
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 13826
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 11326
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 13826
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 11326
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 13826
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 13826
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 13826
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 11326
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 11326
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 13826
                  },
                  {
                    "year": 2023,
                    "month": 7,
                    "search_volume": 13822
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}

**Description of the fields for setting a task:**

| Field name | Type | Description |
| --- | --- | --- |
| `keywords` | array | _keywords_<br>**required field**<br>UTF-8 encoding<br>The maximum number of keywords you can specify: 200.<br>The keywords will be converted to lowercase format<br>learn more about rules and limitations of `keyword` and `keywords` fields in DataForSEO APIs in this [Help Center article](https://dataforseo.com/help-center/rules-and-limitations-of-keyword-and-keywords-fields-in-dataforseo-apis) |  |
| `location_name` | string | _full name of the location_<br>**required field if you don’t specify** `location_code`<br>**Note:** it is required to specify either `location_name` or `location_code`<br>you can receive the list of available locations with their `location_name` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`United Kingdom` |  |
| `location_code` | integer | _unique location identifier_<br>**required field if you don’t specify** `location_name`<br>**Note:** it is required to specify either `location_name` or `location_code`<br>you can receive the list of available locations with their `location_code` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`2840` |  |
| `language_name` | string | _full name of the language_<br>optional field<br>if you use this field, you don’t need to specify `language_code`<br>you can receive the list of available languages with their `language_name` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`English`<br>**Note:** if omitted, results default to the language with the most keyword records in the specified location;<br>refer to the `available_languages.keywords` field of the [Locations and Languages endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages) to determine the default language |  |
| `language_code` | string | _language code_<br>optional field<br>if you use this field, you don’t need to specify `language_name`<br>you can receive the list of available languages with their `language_code` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`en`<br>**Note:** if omitted, results default to the language with the most keyword records in the specified location;<br>refer to the `available_languages.keywords` field of the [Locations and Languages endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages) to determine the default language |  |
| `closely_variants` | boolean | _search mode_<br>optional field<br>if set to `true` the results will be based on the phrase-match search algorithm<br>if set to `false` the results will be based on the broad-match search algorithm<br>default value: `false` |  |
| `ignore_synonyms` | boolean | _ignore highly similar keywords_<br>optional field<br>if set to `true` only core keywords will be returned, all highly similar keywords will be excluded;<br>default value: `false` |  |
| `include_serp_info` | boolean | _include data from SERP for each keyword_<br>optional field<br>if set to `true`, we will return a `serp_info` array containing SERP data (number of search results, relevant URL, and SERP features) for every keyword in the response<br>default value: `false` |  |
| `include_clickstream_data` | boolean | _include or exclude data from clickstream-based metrics in the result_<br>optional field<br>if the parameter is set to `true`, you will receive `clickstream_keyword_info`, `keyword_info_normalized_with_clickstream`, and `keyword_info_normalized_with_bing` fields in the response<br>default value: `false`<br>with this parameter enabled, you will be charged double the price for the request<br>learn more about how clickstream-based metrics are calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `limit` | integer | _the maximum number of keywords in the results array_<br>optional field<br>default value: `700`<br>maximum value: `1000` |  |
| `offset` | integer | _offset in the results array of returned keywords_<br>optional field<br>default value: `0`<br>if you specify the `10` value, the first ten keywords in the results array will be omitted and the data will be provided for the successive keywords |  |
| `offset_token` | string | _offset token for subsequent requests_<br>optional field<br>provided in the identical filed of the response to each request;<br>use this parameter to avoid timeouts while trying to obtain over 10,000 results in a single request;<br>by specifying the unique `offset_token` value from the response array, you will get the subsequent results of the initial task;<br>`offset_token` values are unique for each subsequent task<br>**Note:** if the `offset_token` is specified in the request, all other parameters except `limit` will not be taken into account when processing a task. |  |
| `filters` | array | _array of results filtering parameters_<br>optional field<br>**you can add several filters at once (8 filters maximum)**<br>you should set a logical operator `and`, `or` between the conditions<br>the following operators are supported:<br>`regex`, `not_regex`, `<`, `<=`, `>`, `>=`, `=`, `<>`, `in`, `not_in`, `match`, `not_match`, `ilike`, `not_ilike`, `like`, `not_like`<br>you can use the `%` operator with `like` and `not_like`,as well as `ilike`, `not_ilike` to match any string of zero or more characters<br>**note that you can not filter the results by `relevance`**<br>example:<br>`["keyword_info.search_volume",">",0]`<br>`[["keyword_info.search_volume","in",[0,1000]],<br>"and",<br>["keyword_info.competition_level","=","LOW"]]`<br>`[["keyword_info.search_volume",">",100],<br>"and",<br>[["keyword_info.cpc","<",0.5],<br>"or",<br>["keyword_info.high_top_of_page_bid","<=",0.5]]]`<br>for more information about filters, please refer to [Dataforseo Labs – Filters](https://docs.dataforseo.com/v3/dataforseo_labs/filters) or this [help center guide](https://dataforseo.com/help-center/how-to-use-filters-in-dataforseo-labs-api) |  |
| `order_by` | array | _results sorting rules_<br>optional field<br>you can use the same values as in the `filters` array to sort the results<br>possible sorting types:<br>`asc` – results will be sorted in the ascending order<br>`desc` – results will be sorted in the descending order<br>you should use a comma to set up a sorting parameter<br>default rule:<br>`["relevance,desc"]`<br>relevance is used as the default sorting rule to provide you with the closest keyword ideas. We recommend using this sorting rule to get highly-relevant search terms. **Note** that `relevance` is only our internal system identifier, so **it can not be used as a filter**, and you will not find this field in the `result` array. The relevance score is based on a similar principle as used in [the Keywords For Keywords](https://docs.dataforseo.com/v3/keywords_data/google/keywords_for_keywords/live/?php) endpoint.<br>**note that you can set no more than three sorting rules in a single request**<br>you should use a comma to separate several sorting rules<br>example:<br>`["relevance,desc","keyword_info.search_volume,desc"]` |  |
| `tag` | string | _user-defined task identifier_<br>optional field<br>_the character limit is 255_<br>you can use this parameter to identify the task and match it with the result<br>you will find the specified `tag` value in the `data` object of the response |  |

‌

As a response of the API server, you will receive [JSON](https://en.wikipedia.org/wiki/JSON)-encoded data containing a `tasks` array with the information specific to the set tasks.

**Description of the fields in the results array:**

| Field name | Type | Description |
| --- | --- | --- |
| `version` | string | _the current version of the API_ |  |
| `status_code` | integer | _general status code_<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors)<br>**Note:** we strongly recommend designing a necessary system for handling related exceptional or error conditions |  |
| `status_message` | string | _general informational message_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `time` | string | _execution time, seconds_ |  |
| `cost` | float | _total tasks cost, USD_ |  |
| `tasks_count` | integer | _the number of tasks in the **`tasks`** array_ |  |
| `tasks_error` | integer | _the number of tasks in the **`tasks`** array returned with an error_ |  |
| **`tasks`** | array | _array of tasks_ |  |
| `id` | string | _task identifier_<br>**unique task identifier in our system in the [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format** |  |
| `status_code` | integer | _status code of the task_<br>generated by DataForSEO; can be within the following range: 10000-60000<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `status_message` | string | _informational message of the task_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix-errors/) |  |
| `time` | string | _execution time, seconds_ |  |
| `cost` | float | _cost of the task, USD_ |  |
| `result_count` | integer | _number of elements in the `result` array_ |  |
| `path` | array | _URL path_ |  |
| `data` | object | _contains the same parameters that you specified in the POST request_ |  |
| **`result`** | array | _array of results_ |  |
| `se_type` | string | _search engine type_ |  |
| `seed_keywords` | array | _keywords in a POST array_<br>**keywords are returned with decoded %## (plus character ‘+’ will be decoded to a space character)** |  |
| `location_code` | integer | _location code in a POST array_ |  |
| `language_code` | string | _language code in a POST array_ |  |
| `total_count` | integer | _total number of results relevant to your request in our database_ |  |
| `items_count` | integer | _number of results returned in the `items` array_ |  |
| `offset` | integer | _current offset value_ |  |
| `offset_token` | string | _offset token for subsequent requests_<br>you can use the string provided in this field to get the subsequent results of the initial task;<br>**note:** `offset_token` values are unique for each subsequent task |  |
| `items` | array | _contains keyword ideas and related data_ |  |
| `se_type` | string | _search engine type_ |  |
| `keyword` | string | _returned keyword idea_ |  |
| `location_code` | integer | _location code in a POST array_ |  |
| `language_code` | string | _language code in a POST array_ |  |
| `keyword_info` | object | _keyword data for the returned keyword idea_ |  |
| `se_type` | string | _search engine type_ |  |
| `last_updated_time` | string | _date and time when keyword data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `competition` | float | _competition_<br>represents the relative amount of competition associated with the given keyword;<br>the value is based on Google Ads data and can be between 0 and 1 (inclusive) |  |
| `competition_level` | string | _competition level_<br>represents the relative level of competition associated with the given keyword in paid SERP only;<br>possible values: `LOW`, `MEDIUM`, `HIGH`<br>if competition level is unknown, the value is `null`;<br>learn more about the metric in [this help center article](https://dataforseo.com/help-center/what-is-competition) |  |
| `cpc` | float | _cost-per-click_<br>represents the average cost per click (USD) historically paid for the keyword |  |
| `search_volume` | integer | _average monthly search volume rate_<br>represents the (approximate) number of searches for the given keyword idea on google.com |  |
| `low_top_of_page_bid` | float | _minimum bid for the ad to be displayed at the top of the first page_<br>indicates the value greater than about 20% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)<br>the value may differ depending on the location specified in a POST request |  |
| `high_top_of_page_bid` | float | _maximum bid for the ad to be displayed at the top of the first page_<br>indicates the value greater than about 80% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)<br>the value may differ depending on the location specified in a POST request |  |
| `categories` | array | _product and service categories_<br>you can download the [full list of possible categories](https://cdn.dataforseo.com/v3/categories/categories_dataforseo_labs_2023_10_25.csv) |  |
| `monthly_searches` | array | _monthly searches_<br>represents the (approximate) number of searches on this keyword idea (as available for the past twelve months), targeted to the specified geographic locations |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _monthly average search volume rate_ |  |
| `search_volume_trend` | object | _search volume trend changes_<br>represents search volume change in percent compared to the previous period |  |
| `monthly` | integer | _search volume change in percent compared to the previous month_ |  |
| `quarterly` | integer | _search volume change in percent compared to the previous quarter_ |  |
| `yearly` | integer | _search volume change in percent compared to the previous year_ |  |
| `clickstream_keyword_info` | object | _clickstream data for the returned keyword_<br>to retrieve results for this field, the parameter `include_clickstream_data` must be set to `true` |  |
| `search_volume` | integer | _monthly average clickstream search volume rate_ |  |
| `last_updated_time` | string | _date and time when the clickstream dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” |  |
| `gender_distribution` | object | _distribution of estimated clickstream-based metrics by gender_<br>learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `female` | integer | _number of female users in the relevant clickstream dataset_ |  |
| `male` | integer | _number of male users in the relevant clickstream dataset_ |  |
| `age_distribution` | object | _distribution of clickstream-based metrics by age_<br>learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `18-24` | integer | _number of users in the relevant clickstream dataset that fall within the 18-24 age range_ |  |
| `25-34` | integer | _number of users in the relevant clickstream dataset that fall within the 25-34 age range_ |  |
| `35-44` | integer | _number of users in the relevant clickstream dataset that fall within the 35-44 age range_ |  |
| `45-54` | integer | _number of users in the relevant clickstream dataset that fall within the 45-54 age range_ |  |
| `55-64` | integer | _number of users in the relevant clickstream dataset that fall within the 55-64 age range_ |  |
| `monthly_searches` | array | _monthly clickstream search volume rates_<br>array of objects with clickstream search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _clickstream-based search volume rate in a certain month of a year_ |  |
| `keyword_properties` | object | _additional information about the keyword_ |  |
| `se_type` | string | _search engine type_ |  |
| `core_keyword` | string | _main keyword in a group_<br>contains the main keyword in a group determined by the synonym clustering algorithm<br>if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` |  |
| `synonym_clustering_algorithm` | string | _the algorithm used to identify synonyms_<br>possible values:<br>`keyword_metrics` – indicates the algorithm based on `keyword_info` parameters<br>`text_processing` – indicates the text-based algorithm<br>if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` |  |
| `keyword_difficulty` | integer | _difficulty of ranking in the first top-10 organic results for a keyword_<br>indicates the chance of getting in top-10 organic results for a keyword on a logarithmic scale from 0 to 100;<br>calculated by analysing, among other parameters, link profiles of the first 10 pages in SERP;<br>learn more about the metric in [this help center guide](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated) |  |
| `detected_language` | string | _detected language of the keyword_<br>indicates the language of the keyword as identified by our system |  |
| `is_another_language` | boolean | _detected language of the keyword is different from the set language_<br>if `true`, the language set in the request does not match the language determined by our system for a given keyword |  |
| `serp_info` | object | _SERP data_<br>the value will be `null` if you didn’t set the field `include_serp_info` to `true` in the POST array or if there is no SERP data for this keyword in our database |  |
| `se_type` | string | _search engine type_ |  |
| `check_url` | string | _direct URL to search engine results_<br>you can use it to make sure that we provided accurate results |  |
| `serp_item_types` | array | _types of search results in SERP_<br>contains types of search results (items) found in SERP<br>possible item types:<br>`answer_box`, `app`, `carousel`, `multi_carousel`, `featured_snippet`, `google_flights`, `google_reviews`, `third_party_reviews`, `google_posts`, `images`, `jobs`, `knowledge_graph`, `local_pack`, `hotels_pack`, `map`, `organic`, `paid`, `people_also_ask`, `related_searches`, `people_also_search`, `shopping`, `top_stories`, `twitter`, `video`, `events`, `mention_carousel`, `recipes`, `top_sights`, `scholarly_articles`, `popular_products`, `podcasts`, `questions_and_answers`, `find_results_on`, `stocks_box`, `visual_stories`, `commercial_units`, `local_services`, `google_hotels`, `math_solver`, `currency_box`, `product_considerations`, `found_on_web`, `short_videos`, `refine_products`, `explore_brands`, `perspectives`, `discussions_and_forums`, `compare_sites`, `courses`, `ai_overview`;<br>**note** that the actual results will be returned only for `organic`, `paid`, `featured_snippet`, and `local_pack` elements |  |
| `se_results_count` | string | _number of search results for the returned keyword_ |  |
| `last_updated_time` | string | _date and time when SERP data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `previous_updated_time` | string | _previous to the most recent date and time when SERP data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-10-15 12:57:46 +00:00` |  |
| `avg_backlinks_info` | object | _backlink data for the returned keyword_<br>this object provides the average number of backlinks, referring pages and domains, as well as the average rank values among the top-10 webpages ranking organically for the keyword |  |
| `se_type` | string | _search engine type_ |  |
| `backlinks` | float | _average number of backlinks_ |  |
| `dofollow` | float | _average number of dofollow links_ |  |
| `referring_pages` | float | _average number of referring pages_ |  |
| `referring_domains` | float | _average number of referring domains_ |  |
| `referring_main_domains` | float | _average number of referring main domains_ |  |
| `rank` | float | _average rank_<br>learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) |  |
| `main_domain_rank` | float | _average main domain rank_<br>learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) |  |
| `last_updated_time` | string | _date and time when backlink data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `search_intent_info` | object | _search intent info for the returned keyword_<br>learn about search intent in this [help center article](https://dataforseo.com/help-center/search-intent-and-its-types) |  |
| `se_type` | string | _search engine type_<br>possible values: `google` |  |
| `main_intent` | string | _main search intent_<br>possible values: `informational`, `navigational`, `commercial`, `transactional` |  |
| `foreign_intent` | array | _supplementary search intents_<br>possible values: `informational`, `navigational`, `commercial`, `transactional` |  |
| `last_updated_time` | string | _date and time when search intent data was last updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| **`keyword_info_normalized_with_bing`** | object | _contains keyword search volume normalized with Bing search volume_ |  |
| `last_updated_time` | string | _date and time when the dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `search_volume` | integer | _current search volume rate of a keyword_ |  |
| `is_normalized` | boolean | _keyword info is normalized_<br>if `true`, values are normalized with Bing data |  |
| `monthly_searches` | integer | _monthly search volume rates_<br>array of objects with search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _search volume rate in a certain month of a year_ |  |
| **`keyword_info_normalized_with_clickstream`** | object | _contains keyword search volume normalized with clickstream data_ |  |
| `last_updated_time` | string | _date and time when the dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `search_volume` | integer | _current search volume rate of a keyword_ |  |
| `is_normalized` | boolean | _keyword info is normalized_<br>if `true`, values are normalized with clickstream data |  |
| `monthly_searches` | integer | _monthly search volume rates_<br>array of objects with search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _search volume rate in a certain month of a year_ |  |


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


**`POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live`**

Your account will be charged for each request.

The cost can be calculated on the [Pricing](https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api "Pricing") page.

All POST data should be sent in the [JSON](https://en.wikipedia.org/wiki/JSON) format (UTF-8 encoding). The task setting is done using the POST method. When setting a task, you should send all task parameters in the task array of the generic POST array. You can send up to 2000 API calls per minute. The maximum number of requests that can be sent simultaneously is limited to 30.

You can specify the number of results you want to retrieve, filter and sort them.

Below you will find a detailed description of the fields you can use for setting a task.

**Code**

{
  "version": "0.1.20240801",
  "status_code": 20000,
  "status_message": "Ok.",
  "time": "0.2704 sec.",
  "cost": 0.0101,
  "tasks_count": 1,
  "tasks_error": 0,
  "tasks": [
    {
      "id": "08221704-1535-0399-0000-0acd15b387ff",
      "status_code": 20000,
      "status_message": "Ok.",
      "time": "0.2019 sec.",
      "cost": 0.0101,
      "result_count": 1,
      "path": [
        "v3",
        "dataforseo_labs",
        "google",
        "keyword_suggestions",
        "live"
      ],
      "data": {
        "api": "dataforseo_labs",
        "function": "keyword_suggestions",
        "se_type": "google",
        "keyword": "phone",
        "location_code": 2840,
        "language_code": "en",
        "include_serp_info": true,
        "include_seed_keyword": true,
        "limit": 1
      },
      "result": [
        {
          "se_type": "google",
          "seed_keyword": "phone",
          "seed_keyword_data": {
            "se_type": "google",
            "keyword": "phone",
            "location_code": 2840,
            "language_code": "en",
            "keyword_info": {
              "se_type": "google",
              "last_updated_time": "2024-08-11 13:24:34 +00:00",
              "competition": 1,
              "competition_level": "HIGH",
              "cpc": 5.98,
              "search_volume": 368000,
              "low_top_of_page_bid": 3.08,
              "high_top_of_page_bid": 10.5,
              "categories": [
                10007,
                10878,
                12133,
                13381
              ],
              "monthly_searches": [
                {
                  "year": 2024,
                  "month": 7,
                  "search_volume": 450000
                },
                {
                  "year": 2024,
                  "month": 6,
                  "search_volume": 368000
                },
                {
                  "year": 2024,
                  "month": 5,
                  "search_volume": 368000
                },
                {
                  "year": 2024,
                  "month": 4,
                  "search_volume": 368000
                },
                {
                  "year": 2024,
                  "month": 3,
                  "search_volume": 368000
                },
                {
                  "year": 2024,
                  "month": 2,
                  "search_volume": 368000
                },
                {
                  "year": 2024,
                  "month": 1,
                  "search_volume": 368000
                },
                {
                  "year": 2023,
                  "month": 12,
                  "search_volume": 368000
                },
                {
                  "year": 2023,
                  "month": 11,
                  "search_volume": 368000
                },
                {
                  "year": 2023,
                  "month": 10,
                  "search_volume": 368000
                },
                {
                  "year": 2023,
                  "month": 9,
                  "search_volume": 368000
                },
                {
                  "year": 2023,
                  "month": 8,
                  "search_volume": 368000
                }
              ],
              "search_volume_trend": {
                "monthly": 22,
                "quarterly": 22,
                "yearly": 0
              }
            }
          },
          "clickstream_keyword_info": null,
          "serp_info": {
            "se_type": "google",
            "check_url": "https://www.google.com/search?q=phone&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",
            "serp_item_types": [
              "popular_products",
              "images",
              "organic",
              "product_considerations",
              "refine_products",
              "top_stories",
              "related_searches"
            ],
            "se_results_count": 19880000000,
            "last_updated_time": "2024-07-15 00:43:34 +00:00",
            "previous_updated_time": "2024-05-18 22:29:28 +00:00"
          },
          "keyword_properties": {
            "se_type": "google",
            "core_keyword": null,
            "synonym_clustering_algorithm": "text_processing",
            "keyword_difficulty": 83,
            "detected_language": "en",
            "is_another_language": false
          },
          "search_intent_info": {
            "se_type": "google",
            "main_intent": "navigational",
            "foreign_intent": [
              "commercial"
            ],
            "last_updated_time": "2023-03-02 03:54:21 +00:00"
          },
          "avg_backlinks_info": {
            "se_type": "google",
            "backlinks": 6835.7,
            "dofollow": 3775.6,
            "referring_pages": 5352.2,
            "referring_domains": 1100.3,
            "referring_main_domains": 955.1,
            "rank": 369.3,
            "main_domain_rank": 681.2,
            "last_updated_time": "2024-07-14 21:43:39 +00:00"
          },
          "keyword_info_normalized_with_bing": {
            "last_updated_time": "2024-08-17 01:41:37 +00:00",
            "search_volume": 324416,
            "is_normalized": true,
            "monthly_searches": [
              {
                "year": 2024,
                "month": 7,
                "search_volume": 396705
              },
              {
                "year": 2024,
                "month": 6,
                "search_volume": 324416
              },
              {
                "year": 2024,
                "month": 5,
                "search_volume": 324416
              },
              {
                "year": 2024,
                "month": 4,
                "search_volume": 324416
              },
              {
                "year": 2024,
                "month": 3,
                "search_volume": 324416
              },
              {
                "year": 2024,
                "month": 2,
                "search_volume": 324416
              },
              {
                "year": 2024,
                "month": 1,
                "search_volume": 324416
              },
              {
                "year": 2023,
                "month": 12,
                "search_volume": 324416
              },
              {
                "year": 2023,
                "month": 11,
                "search_volume": 324416
              },
              {
                "year": 2023,
                "month": 10,
                "search_volume": 324416
              },
              {
                "year": 2023,
                "month": 9,
                "search_volume": 324416
              },
              {
                "year": 2023,
                "month": 8,
                "search_volume": 324416
              }
            ]
          },
          "keyword_info_normalized_with_clickstream": {
            "last_updated_time": "2024-08-11 13:24:34 +00:00",
            "search_volume": 368000,
            "is_normalized": true,
            "monthly_searches": [
              {
                "year": 2024,
                "month": 7,
                "search_volume": 450000
              },
              {
                "year": 2024,
                "month": 6,
                "search_volume": 368000
              },
              {
                "year": 2024,
                "month": 5,
                "search_volume": 368000
              },
              {
                "year": 2024,
                "month": 4,
                "search_volume": 368000
              },
              {
                "year": 2024,
                "month": 3,
                "search_volume": 368000
              },
              {
                "year": 2024,
                "month": 2,
                "search_volume": 368000
              },
              {
                "year": 2024,
                "month": 1,
                "search_volume": 368000
              },
              {
                "year": 2023,
                "month": 12,
                "search_volume": 368000
              },
              {
                "year": 2023,
                "month": 11,
                "search_volume": 368000
              },
              {
                "year": 2023,
                "month": 10,
                "search_volume": 368000
              },
              {
                "year": 2023,
                "month": 9,
                "search_volume": 368000
              },
              {
                "year": 2023,
                "month": 8,
                "search_volume": 368000
              }
            ]
          }
        },
        {
          "location_code": 2840,
          "language_code": "en",
          "total_count": 3488300,
          "items_count": 1,
          "offset": 0,
          "offset_token": "eyJDdXJyZW50T2Zmc2V0IjoxLCJSZXF1ZXN0RGF0YSI6eyJrZXl3b3JkIjoicGhvbmUiLCJpbmNsdWRlX3NlZWRfa2V5d29yZCI6dHJ1ZSwiZnVsbF9tYXRjaCI6ZmFsc2UsImxvYWRfc2VycF9pbmZvIjp0cnVlLCJzZWFyY2hfYWZ0ZXJfdG9rZW4iOm51bGwsImlnbm9yZV9zeW5vbnltcyI6ZmFsc2UsImxhbmd1YWdlIjoiZW4iLCJzZWFyY2hfZW5naW5lIjoiZ29vZ2xlIiwibG9jYXRpb24iOjI4NDAsInVzZV9uZXdfY2F0ZWdvcmllcyI6dHJ1ZSwib3JkZXJfYnkiOnsib3JkZXJfZmllbGQiOiJrZXl3b3JkX2luZm8uc2VhcmNoX3ZvbHVtZSIsIm9yZGVyX3R5cGUiOiJEZXNjIiwibmV4dCI6bnVsbH0sImxpbWl0IjoxLCJvZmZzZXQiOjAsImFpZCI6MTUzNX0sIlJhd1F1ZXJ5IjpudWxsLCJJZCI6Ijc0MjcwOGQwLWZjMjgtNDMwZi04NzA3LTRhZmVjYmJkNDgwZCIsIlNlYXJjaEFmdGVyRGF0YSI6WzE4MzAwMDAsIjkwYzI4YjVjLWVmNWQtNGUwMi04MGU2LTBkYThkZjQyZDY0NyJdfQ==",
          "items": [
            {
              "se_type": "google",
              "keyword": "boost cell phone",
              "location_code": 2840,
              "language_code": "en",
              "keyword_info": {
                "se_type": "google",
                "last_updated_time": "2024-08-12 23:31:45 +00:00",
                "competition": 0.96,
                "competition_level": "HIGH",
                "cpc": 1.47,
                "search_volume": 1830000,
                "low_top_of_page_bid": 0.85,
                "high_top_of_page_bid": 10.44,
                "categories": [
                  10007,
                  10878,
                  12161,
                  13381
                ],
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 2240000
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 2240000
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 1830000
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 1830000
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 2240000
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 1830000
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 1830000
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 2240000
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 2240000
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 1830000
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 1830000
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 1830000
                  }
                ],
                "search_volume_trend": {
                  "monthly": 22,
                  "quarterly": 22,
                  "yearly": 0
                }
              },
              "clickstream_keyword_info": null,
              "keyword_properties": {
                "se_type": "google",
                "core_keyword": null,
                "synonym_clustering_algorithm": "text_processing",
                "keyword_difficulty": 0,
                "detected_language": "en",
                "is_another_language": false
              },
              "serp_info": {
                "se_type": "google",
                "check_url": "https://www.google.com/search?q=boost%20cell%20phone&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",
                "serp_item_types": [
                  "organic",
                  "people_also_ask",
                  "local_pack",
                  "popular_products",
                  "top_sights",
                  "video",
                  "images",
                  "related_searches"
                ],
                "se_results_count": 115000000,
                "last_updated_time": "2024-08-04 08:25:36 +00:00",
                "previous_updated_time": "2024-06-22 17:54:36 +00:00"
              },
              "avg_backlinks_info": {
                "se_type": "google",
                "backlinks": 4739.3,
                "dofollow": 2334.9,
                "referring_pages": 4121.3,
                "referring_domains": 210.3,
                "referring_main_domains": 184.2,
                "rank": 113.1,
                "main_domain_rank": 512.4,
                "last_updated_time": "2024-08-04 08:25:38 +00:00"
              },
              "search_intent_info": {
                "se_type": "google",
                "main_intent": "transactional",
                "foreign_intent": null,
                "last_updated_time": "2023-12-14 04:27:21 +00:00"
              },
              "keyword_info_normalized_with_bing": {
                "last_updated_time": "2024-08-17 06:05:32 +00:00",
                "search_volume": 2893,
                "is_normalized": true,
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 3541
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 3541
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 2893
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 2893
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 3541
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 2893
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 2893
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 3541
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 3541
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 2893
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 2893
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 2893
                  },
                  {
                    "year": 2023,
                    "month": 7,
                    "search_volume": 2778
                  }
                ]
              },
              "keyword_info_normalized_with_clickstream": {
                "last_updated_time": "2024-08-17 06:05:32 +00:00",
                "search_volume": 197,
                "is_normalized": true,
                "monthly_searches": [
                  {
                    "year": 2024,
                    "month": 7,
                    "search_volume": 242
                  },
                  {
                    "year": 2024,
                    "month": 6,
                    "search_volume": 242
                  },
                  {
                    "year": 2024,
                    "month": 5,
                    "search_volume": 197
                  },
                  {
                    "year": 2024,
                    "month": 4,
                    "search_volume": 197
                  },
                  {
                    "year": 2024,
                    "month": 3,
                    "search_volume": 242
                  },
                  {
                    "year": 2024,
                    "month": 2,
                    "search_volume": 197
                  },
                  {
                    "year": 2024,
                    "month": 1,
                    "search_volume": 197
                  },
                  {
                    "year": 2023,
                    "month": 12,
                    "search_volume": 242
                  },
                  {
                    "year": 2023,
                    "month": 11,
                    "search_volume": 242
                  },
                  {
                    "year": 2023,
                    "month": 10,
                    "search_volume": 197
                  },
                  {
                    "year": 2023,
                    "month": 9,
                    "search_volume": 197
                  },
                  {
                    "year": 2023,
                    "month": 8,
                    "search_volume": 197
                  },
                  {
                    "year": 2023,
                    "month": 7,
                    "search_volume": 190
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}

**Description of the fields for setting a task:**

| Field name | Type | Description |
| --- | --- | --- |
| `keyword` | string | _keyword_<br>**required field**<br>UTF-8 encoding<br>the keywords will be converted to lowercase format;<br>learn more about rules and limitations of `keyword` and `keywords` fields in DataForSEO APIs in this [Help Center article](https://dataforseo.com/help-center/rules-and-limitations-of-keyword-and-keywords-fields-in-dataforseo-apis) |  |
| `location_name` | string | _full name of the location_<br>optional field<br>if you use this field, you don’t need to specify `location_code`<br>you can receive the list of available locations with their `location_name` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>ignore this field to get the results for all available locations<br>example:<br>`United Kingdom` |  |
| `location_code` | integer | _location code_<br>optional field<br>if you use this field, you don’t need to specify `location_name`<br>you can receive the list of available locations with their `location_code` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>ignore this field to get the results for all available locations<br>example:<br>`2840` |  |
| `language_name` | string | _full name of the language_<br>optional field<br>if you use this field, you don’t need to specify `language_code`<br>you can receive the list of available languages with their `language_name` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`English`<br>**Note:** if omitted, results default to the language with the most keyword records in the specified location;<br>refer to the `available_languages.keywords` field of the [Locations and Languages endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages) to determine the default language |  |
| `language_code` | string | _language code_<br>optional field<br>if you use this field, you don’t need to specify `language_name`<br>you can receive the list of available languages with their `language_code` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`en`<br>**Note:** if omitted, results default to the language with the most keyword records in the specified location;<br>refer to the `available_languages.keywords` field of the [Locations and Languages endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages) to determine the default language |  |
| `include_seed_keyword` | boolean | _include data for the seed keyword_<br>optional field<br>if set to `true`, data for the seed keyword specified in the `keyword` field will be provided in the `seed_keyword_data` array of the response<br>default value: `false` |  |
| `include_serp_info` | boolean | _include data from SERP for each keyword_<br>optional field<br>if set to `true`, we will return a `serp_info` array containing SERP data (number of search results, relevant URL, and SERP features) for every keyword in the response<br>default value: `false` |  |
| `include_clickstream_data` | boolean | _include or exclude data from clickstream-based metrics in the result_<br>optional field<br>if the parameter is set to `true`, you will receive `clickstream_keyword_info`, `keyword_info_normalized_with_clickstream`, and `keyword_info_normalized_with_bing` fields in the response<br>default value: `false`<br>with this parameter enabled, you will be charged double the price for the request<br>learn more about how clickstream-based metrics are calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `exact_match` | boolean | _search for the exact phrase_<br>optional field<br>if set to `true`, the returned keywords will include the exact keyword phrase you specified, with potentially other words before or after that phrase<br>default value: `false` |  |
| `ignore_synonyms` | boolean | _ignore highly similar keywords_<br>optional field<br>if set to `true` only core keywords will be returned, all highly similar keywords will be excluded;<br>default value: `false` |  |
| `filters` | array | _array of results filtering parameters_<br>optional field<br>**you can add several filters at once (8 filters maximum)**<br>you should set a logical operator `and`, `or` between the conditions<br>the following operators are supported:<br>`regex`, `not_regex`, `<`, `<=`, `>`, `>=`, `=`, `<>`, `in`, `not_in`, `match`, `not_match`, `ilike`, `not_ilike`, `like`, `not_like`<br>you can use the `%` operator with `like` and `not_like`, as well as `ilike` and `not_ilike` to match any string of zero or more characters<br>example:<br>`["keyword_info.search_volume",">",0]`<br>`[["keyword_info.search_volume","in",[0,1000]],<br>"and",<br>["keyword_info.competition_level","=","LOW"]]` `[["keyword_info.search_volume",">",100],<br>"and",<br>[["keyword_info.cpc","<",0.5],<br>"or",<br>["keyword_info.high_top_of_page_bid","<=",0.5]]]`<br>for more information about filters, please refer to [Dataforseo Labs – Filters](https://docs.dataforseo.com/v3/dataforseo_labs/filters) or this [help center guide](https://dataforseo.com/help-center/how-to-use-filters-in-dataforseo-labs-api) |  |
| `order_by` | array | _results sorting rules_<br>optional field<br>you can use the same values as in the `filters` array to sort the results<br>possible sorting types:<br>`asc` – results will be sorted in the ascending order<br>`desc` – results will be sorted in the descending order<br>a comma is used as a separator<br>example:<br>`["keyword_info.competition,desc"]`<br>default rule:<br>`["keyword_info.search_volume,desc"]`<br>**note that you can set no more than three sorting rules in a single request**<br>you should use a comma to separate several sorting rules<br>example:<br>`["keyword_info.search_volume,desc","keyword_info.cpc,desc"]` |  |
| `limit` | integer | _the maximum number of returned keywords_<br>optional field<br>default value: `100`<br>maximum value: `1000` |  |
| `offset` | integer | _offset in the results array of returned keywords_<br>optional field<br>default value: `0`<br>if you specify the `10` value, the first ten keywords in the results array will be omitted and the data will be provided for the successive keywords |  |
| `offset_token` | string | _offset token for subsequent requests_<br>optional field<br>provided in the identical filed of the response to each request;<br>use this parameter to avoid timeouts while trying to obtain over 10,000 results in a single request;<br>by specifying the unique `offset_token` value from the response array, you will get the subsequent results of the initial task;<br>`offset_token` values are unique for each subsequent task<br>**Note:** if the `offset_token` is specified in the request, all other parameters except `limit` will not be taken into account when processing a task. |  |
| `tag` | string | _user-defined task identifier_<br>optional field<br>_the character limit is 255_<br>you can use this parameter to identify the task and match it with the result<br>you will find the specified `tag` value in the `data` object of the response |  |

‌

As a response of the API server, you will receive [JSON](https://en.wikipedia.org/wiki/JSON)-encoded data containing a `tasks` array with the information specific to the set tasks.

**Description of the fields in the results array:**

| Field name | Type | Description |
| --- | --- | --- |
| `version` | string | _the current version of the API_ |  |
| `status_code` | integer | _general status code_<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors)<br>**Note:** we strongly recommend designing a necessary system for handling related exceptional or error conditions |  |
| `status_message` | string | _general informational message_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `time` | string | _execution time, seconds_ |  |
| `cost` | float | _total tasks cost, USD_ |  |
| `tasks_count` | integer | _the number of tasks in the **`tasks`** array_ |  |
| `tasks_error` | integer | _the number of tasks in the **`tasks`** array returned with an error_ |  |
| **`tasks`** | array | _array of tasks_ |  |
| `id` | string | _task identifier_<br>**unique task identifier in our system in the [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format** |  |
| `status_code` | integer | _status code of the task_<br>generated by DataForSEO; can be within the following range: 10000-60000<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `status_message` | string | _informational message of the task_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix-errors/) |  |
| `time` | string | _execution time, seconds_ |  |
| `cost` | float | _cost of the task, USD_ |  |
| `result_count` | integer | _number of elements in the `result` array_ |  |
| `path` | array | _URL path_ |  |
| `data` | object | _contains the same parameters that you specified in the POST request_ |  |
| **`result`** | array | _array of results_ |  |
| `se_type` | string | _search engine type_ |  |
| `seed_keyword` | string | _keyword in a POST array_ |  |
| **`seed_keyword_data`** | object | _keyword data for the seed keyword_<br>fields in this object are identical to those of the `items` array |  |
| `location_code` | integer | _location code in a POST array_<br>if there is no data, then the value is `null` |  |
| `language_code` | string | _language code in a POST array_<br>if there is no data, then the value is `null` |  |
| `total_count` | integer | _total amount of results in our database relevant to your request_ |  |
| `items_count` | integer | _the number of results returned in the `items` array_ |  |
| `offset` | integer | _current offset value_ |  |
| `offset_token` | string | _offset token for subsequent requests_<br>you can use the string provided in this field to get the subsequent results of the initial task;<br>**note:** `offset_token` values are unique for each subsequent task |  |
| **`items`** | array | _contains keywords and related data_ |  |
| `se_type` | string | _search engine type_ |  |
| `keyword` | string | _keyword suggestion_ |  |
| `location_code` | integer | _location code in a POST array_ |  |
| `language_code` | string | _language code in a POST array_ |  |
| **`keyword_info`** | object | _keyword data for the returned keyword_ |  |
| `se_type` | string | _search engine type_ |  |
| `last_updated_time` | string | _date and time when keyword data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `competition` | float | _competition_<br>represents the relative amount of competition associated with the given keyword;<br>the value is based on Google Ads data and can be between 0 and 1 (inclusive) |  |
| `competition_level` | string | _competition level_<br>represents the relative level of competition associated with the given keyword in paid SERP only;<br>possible values: `LOW`, `MEDIUM`, `HIGH`<br>if competition level is unknown, the value is `null`;<br>learn more about the metric in [this help center article](https://dataforseo.com/help-center/what-is-competition) |  |
| `cpc` | float | _cost-per-click_<br>represents the average cost per click (USD) historically paid for the keyword |  |
| `search_volume` | integer | _average monthly search volume rate_<br>represents the (approximate) number of searches for the given keyword idea on google.com |  |
| `low_top_of_page_bid` | float | _minimum bid for the ad to be displayed at the top of the first page_<br>indicates the value greater than about 20% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)<br>the value may differ depending on the location specified in a POST request |  |
| `high_top_of_page_bid` | float | _maximum bid for the ad to be displayed at the top of the first page_<br>indicates the value greater than about 80% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)<br>the value may differ depending on the location specified in a POST request |  |
| `categories` | array | _product and service categories_<br>you can download the [full list of possible categories](https://cdn.dataforseo.com/v3/categories/categories_dataforseo_labs_2023_10_25.csv) |  |
| `monthly_searches` | array | _monthly searches_<br>represents the (approximate) number of searches for this keyword idea (as available for the past twelve months), targeted to the specified geographic locations |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _monthly average search volume rate_ |  |
| `search_volume_trend` | object | _search volume trend changes_<br>represents search volume change in percent compared to the previous period |  |
| `monthly` | integer | _search volume change in percent compared to the previous month_ |  |
| `quarterly` | integer | _search volume change in percent compared to the previous quarter_ |  |
| `yearly` | integer | _search volume change in percent compared to the previous year_ |  |
| `clickstream_keyword_info` | object | _clickstream data for the returned keyword_<br>to retrieve results for this field, the parameter `include_clickstream_data` must be set to `true` |  |
| `search_volume` | integer | _monthly average clickstream search volume rate_ |  |
| `last_updated_time` | string | _date and time when the clickstream dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” |  |
| `gender_distribution` | object | _distribution of estimated clickstream-based metrics by gender_<br>learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `female` | integer | _number of female users in the relevant clickstream dataset_ |  |
| `male` | integer | _number of male users in the relevant clickstream dataset_ |  |
| `age_distribution` | object | _distribution of clickstream-based metrics by age_<br>learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `18-24` | integer | _number of users in the relevant clickstream dataset that fall within the 18-24 age range_ |  |
| `25-34` | integer | _number of users in the relevant clickstream dataset that fall within the 25-34 age range_ |  |
| `35-44` | integer | _number of users in the relevant clickstream dataset that fall within the 35-44 age range_ |  |
| `45-54` | integer | _number of users in the relevant clickstream dataset that fall within the 45-54 age range_ |  |
| `55-64` | integer | _number of users in the relevant clickstream dataset that fall within the 55-64 age range_ |  |
| `monthly_searches` | array | _monthly clickstream search volume rates_<br>array of objects with clickstream search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _clickstream-based search volume rate in a certain month of a year_ |  |
| **`keyword_properties`** | object | _additional information about the keyword_ |  |
| `se_type` | string | _search engine type_ |  |
| `core_keyword` | string | _main keyword in a group_<br>contains the main keyword in a group determined by the synonym clustering algorithm<br>if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` |  |
| `synonym_clustering_algorithm` | string | _the algorithm used to identify synonyms_<br>possible values:<br>`keyword_metrics` – indicates the algorithm based on `keyword_info` parameters<br>`text_processing` – indicates the text-based algorithm<br>if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` |  |
| `keyword_difficulty` | integer | _difficulty of ranking in the first top-10 organic results for a keyword_<br>indicates the chance of getting in top-10 organic results for a keyword on a logarithmic scale from 0 to 100;<br>calculated by analysing, among other parameters, link profiles of the first 10 pages in SERP;<br>learn more about the metric in [this help center guide](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated) |  |
| `detected_language` | string | _detected language of the keyword_<br>indicates the language of the keyword as identified by our system |  |
| `is_another_language` | boolean | _detected language of the keyword is different from the set language_<br>if `true`, the language set in the request does not match the language determined by our system for a given keyword |  |
| **`serp_info`** | object | _SERP data_<br>the value will be `null` if you didn’t set the field `include_serp_info` to `true` in the POST array or if there is no SERP data for this keyword in our database |  |
| `se_type` | string | _search engine type_ |  |
| `check_url` | string | _direct URL to search engine results_<br>you can use it to make sure that we provided accurate results |  |
| `serp_item_types` | array | _types of search results in SERP_<br>contains types of search results (items) found in SERP<br>possible item types:<br>`answer_box`, `app`, `carousel`, `multi_carousel`, `featured_snippet`, `google_flights`, `google_reviews`, `third_party_reviews`, `google_posts`, `images`, `jobs`, `knowledge_graph`, `local_pack`, `hotels_pack`, `map`, `organic`, `paid`, `people_also_ask`, `related_searches`, `people_also_search`, `shopping`, `top_stories`, `twitter`, `video`, `events`, `mention_carousel`, `recipes`, `top_sights`, `scholarly_articles`, `popular_products`, `podcasts`, `questions_and_answers`, `find_results_on`, `stocks_box`, `visual_stories`, `commercial_units`, `local_services`, `google_hotels`, `math_solver`, `currency_box`, `product_considerations`, `found_on_web`, `short_videos`, `refine_products`, `explore_brands`, `perspectives`, `discussions_and_forums`, `compare_sites`, `courses`, `ai_overview`;<br>**note** that the actual results will be returned only for `organic`, `paid`, `featured_snippet`, and `local_pack` elements |  |
| `se_results_count` | string | _number of search results for the returned keyword_ |  |
| `last_updated_time` | string | _date and time when SERP data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `previous_updated_time` | string | _previous to the most recent date and time when SERP data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-10-15 12:57:46 +00:00` |  |
| **`avg_backlinks_info`** | object | _backlink data for the returned keyword_<br>this object provides the average number of backlinks, referring pages and domains, as well as the average rank values among the top-10 webpages ranking organically for the keyword |  |
| `se_type` | string | _search engine type_ |  |
| `backlinks` | float | _average number of backlinks_ |  |
| `dofollow` | float | _average number of dofollow links_ |  |
| `referring_pages` | float | _average number of referring pages_ |  |
| `referring_domains` | float | _average number of referring domains_ |  |
| `referring_main_domains` | float | _average number of referring main domains_ |  |
| `rank` | float | _average rank_<br>learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) |  |
| `main_domain_rank` | float | _average main domain rank_<br>learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) |  |
| `last_updated_time` | string | _date and time when backlink data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| **`search_intent_info`** | object | _search intent info for the returned keyword_<br>learn about search intent in this [help center article](https://dataforseo.com/help-center/search-intent-and-its-types) |  |
| `se_type` | string | _search engine type_<br>possible values: `google` |  |
| `main_intent` | string | _main search intent_<br>possible values: `informational`, `navigational`, `commercial`, `transactional` |  |
| `foreign_intent` | array | _supplementary search intents_<br>possible values: `informational`, `navigational`, `commercial`, `transactional` |  |
| `last_updated_time` | string | _date and time when search intent data was last updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| **`keyword_info_normalized_with_bing`** | object | _contains keyword search volume normalized with Bing search volume_ |  |
| `last_updated_time` | string | _date and time when the dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `search_volume` | integer | _current search volume rate of a keyword_ |  |
| `is_normalized` | boolean | _keyword info is normalized_<br>if `true`, values are normalized with Bing data |  |
| `monthly_searches` | integer | _monthly search volume rates_<br>array of objects with search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _search volume rate in a certain month of a year_ |  |
| **`keyword_info_normalized_with_clickstream`** | object | _contains keyword search volume normalized with clickstream data_ |  |
| `last_updated_time` | string | _date and time when the dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `search_volume` | integer | _current search volume rate of a keyword_ |  |
| `is_normalized` | boolean | _keyword info is normalized_<br>if `true`, values are normalized with clickstream data |  |
| `monthly_searches` | integer | _monthly search volume rates_<br>array of objects with search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _search volume rate in a certain month of a year_ |  |

‌## Related Keywords

The Related Keywords endpoint provides keywords appearing in the

["searches related to" SERP element![](https://dataforseo.com/wp-content/uploads/2020/02/window-feature-related-searches.png)](https://docs.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live/?python#)

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

**`POST https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live`**

Your account will be charged for each request.

The cost can be calculated on the [Pricing](https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api "Pricing") page.

All POST data should be sent in the [JSON](https://en.wikipedia.org/wiki/JSON) format (UTF-8 encoding). The task setting is done using the POST method. When setting a task, you should send all task parameters in the task array of the generic POST array. You can send up to 2000 API calls per minute. The maximum number of requests that can be sent simultaneously is limited to 30.

**CODE**

{
  "version": "0.1.20240801",
  "status_code": 20000,
  "status_message": "Ok.",
  "time": "0.0995 sec.",
  "cost": 0.0103,
  "tasks_count": 1,
  "tasks_error": 0,
  "tasks": [
    {
      "id": "08221812-1535-0387-0000-53d53d3e60c5",
      "status_code": 20000,
      "status_message": "Ok.",
      "time": "0.0326 sec.",
      "cost": 0.0103,
      "result_count": 1,
      "path": [
        "v3",
        "dataforseo_labs",
        "google",
        "related_keywords",
        "live"
      ],
      "data": {
        "api": "dataforseo_labs",
        "function": "related_keywords",
        "se_type": "google",
        "keyword": "phone",
        "language_name": "English",
        "location_code": 2840,
        "limit": 3
      },
      "result": [
        {
          "se_type": "google",
          "seed_keyword": "phone",
          "seed_keyword_data": null,
          "location_code": 2840,
          "language_code": "en",
          "total_count": 9,
          "items_count": 3,
          "items": [
            {
              "se_type": "google",
              "keyword_data": {
                "se_type": "google",
                "keyword": "phone",
                "location_code": 2840,
                "language_code": "en",
                "keyword_info": {
                  "se_type": "google",
                  "last_updated_time": "2024-08-11 13:24:34 +00:00",
                  "competition": 1,
                  "competition_level": "HIGH",
                  "cpc": 5.98,
                  "search_volume": 368000,
                  "low_top_of_page_bid": 3.08,
                  "high_top_of_page_bid": 10.5,
                  "categories": [
                    10007,
                    10878,
                    12133,
                    13381
                  ],
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 450000
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 368000
                    }
                  ],
                  "search_volume_trend": {
                    "monthly": 22,
                    "quarterly": 22,
                    "yearly": 0
                  }
                },
                "clickstream_keyword_info": null,
                "keyword_properties": {
                  "se_type": "google",
                  "core_keyword": null,
                  "synonym_clustering_algorithm": "text_processing",
                  "keyword_difficulty": 83,
                  "detected_language": "en",
                  "is_another_language": false
                },
                "serp_info": {
                  "se_type": "google",
                  "check_url": "https://www.google.com/search?q=phone&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",
                  "serp_item_types": [
                    "popular_products",
                    "images",
                    "organic",
                    "product_considerations",
                    "refine_products",
                    "top_stories",
                    "related_searches"
                  ],
                  "se_results_count": 19880000000,
                  "last_updated_time": "2024-07-15 00:43:34 +00:00",
                  "previous_updated_time": "2024-05-18 22:29:28 +00:00"
                },
                "avg_backlinks_info": {
                  "se_type": "google",
                  "backlinks": 6835.7,
                  "dofollow": 3775.6,
                  "referring_pages": 5352.2,
                  "referring_domains": 1100.3,
                  "referring_main_domains": 955.1,
                  "rank": 369.3,
                  "main_domain_rank": 681.2,
                  "last_updated_time": "2024-07-14 21:43:39 +00:00"
                },
                "search_intent_info": {
                  "se_type": "google",
                  "main_intent": "navigational",
                  "foreign_intent": [
                    "commercial"
                  ],
                  "last_updated_time": "2023-03-02 03:54:21 +00:00"
                },
                "keyword_info_normalized_with_bing": {
                  "last_updated_time": "2024-08-17 01:41:37 +00:00",
                  "search_volume": 324416,
                  "is_normalized": true,
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 396705
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 324416
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 324416
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 324416
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 324416
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 324416
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 324416
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 324416
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 324416
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 324416
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 324416
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 324416
                    }
                  ]
                },
                "keyword_info_normalized_with_clickstream": {
                  "last_updated_time": "2024-08-11 13:24:34 +00:00",
                  "search_volume": 368000,
                  "is_normalized": true,
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 450000
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 368000
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 368000
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 368000
                    }
                  ]
                }
              },
              "depth": 0,
              "related_keywords": [
                "phone app",
                "phone call",
                "phone app download",
                "phone call app",
                "phone samsung",
                "phone definition",
                "phone app on android",
                "my phone app"
              ]
            },
            {
              "se_type": "google",
              "keyword_data": {
                "se_type": "google",
                "keyword": "phone call",
                "location_code": 2840,
                "language_code": "en",
                "keyword_info": {
                  "se_type": "google",
                  "last_updated_time": "2024-08-08 14:16:10 +00:00",
                  "competition": 0.07,
                  "competition_level": "LOW",
                  "cpc": 4.23,
                  "search_volume": 27100,
                  "low_top_of_page_bid": 0.92,
                  "high_top_of_page_bid": 7.55,
                  "categories": [
                    10007,
                    10019,
                    10167,
                    10878,
                    11506,
                    11510,
                    12762,
                    13419
                  ],
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 60500
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 27100
                    }
                  ],
                  "search_volume_trend": {
                    "monthly": 22,
                    "quarterly": 22,
                    "yearly": 0
                  }
                },
                "clickstream_keyword_info": null,
                "keyword_properties": {
                  "se_type": "google",
                  "core_keyword": "phone calling",
                  "synonym_clustering_algorithm": "text_processing",
                  "keyword_difficulty": 57,
                  "detected_language": "en",
                  "is_another_language": false
                },
                "serp_info": {
                  "se_type": "google",
                  "check_url": "https://www.google.com/search?q=phone%20call&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",
                  "serp_item_types": [
                    "organic",
                    "people_also_ask",
                    "related_searches"
                  ],
                  "se_results_count": 25270000000,
                  "last_updated_time": "2024-08-04 13:21:19 +00:00",
                  "previous_updated_time": "2024-06-22 22:50:34 +00:00"
                },
                "avg_backlinks_info": {
                  "se_type": "google",
                  "backlinks": 11475.1,
                  "dofollow": 7174.8,
                  "referring_pages": 10754.1,
                  "referring_domains": 884.2,
                  "referring_main_domains": 765,
                  "rank": 329.4,
                  "main_domain_rank": 787.5,
                  "last_updated_time": "2024-08-04 10:21:19 +00:00"
                },
                "search_intent_info": {
                  "se_type": "google",
                  "main_intent": "commercial",
                  "foreign_intent": null,
                  "last_updated_time": "2023-03-02 03:54:30 +00:00"
                },
                "keyword_info_normalized_with_bing": {
                  "last_updated_time": "2024-08-16 12:35:38 +00:00",
                  "search_volume": 19134,
                  "is_normalized": true,
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 19134
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 42717
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 19134
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 19134
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 19134
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 19134
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 19134
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 19134
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 19134
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 19134
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 19134
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 19134
                    }
                  ]
                },
                "keyword_info_normalized_with_clickstream": {
                  "last_updated_time": "2024-08-08 14:16:10 +00:00",
                  "search_volume": 27100,
                  "is_normalized": true,
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 60500
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 27100
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 27100
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 27100
                    }
                  ]
                }
              },
              "depth": 1,
              "related_keywords": [
                "phone call online",
                "phone call app",
                "free phone call",
                "phone app",
                "phone call app download",
                "i want to make a phone call on my phone",
                "phone by google",
                "make a phone call to someone"
              ]
            },
            {
              "se_type": "google",
              "keyword_data": {
                "se_type": "google",
                "keyword": "phone app",
                "location_code": 2840,
                "language_code": "en",
                "keyword_info": {
                  "se_type": "google",
                  "last_updated_time": "2024-08-11 20:06:52 +00:00",
                  "competition": 0.15,
                  "competition_level": "LOW",
                  "cpc": 2.14,
                  "search_volume": 22200,
                  "low_top_of_page_bid": 0.46,
                  "high_top_of_page_bid": 3.16,
                  "categories": [
                    10007,
                    10019,
                    10168,
                    10878,
                    10885,
                    13378,
                    13381
                  ],
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 22200
                    }
                  ],
                  "search_volume_trend": {
                    "monthly": 22,
                    "quarterly": 22,
                    "yearly": 0
                  }
                },
                "clickstream_keyword_info": null,
                "keyword_properties": {
                  "se_type": "google",
                  "core_keyword": "phone for apps",
                  "synonym_clustering_algorithm": "text_processing",
                  "keyword_difficulty": 66,
                  "detected_language": "en",
                  "is_another_language": false
                },
                "serp_info": {
                  "se_type": "google",
                  "check_url": "https://www.google.com/search?q=phone%20app&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc",
                  "serp_item_types": [
                    "organic",
                    "people_also_ask",
                    "images",
                    "related_searches"
                  ],
                  "se_results_count": 25270000000,
                  "last_updated_time": "2024-08-04 13:51:15 +00:00",
                  "previous_updated_time": "2024-06-22 23:19:03 +00:00"
                },
                "avg_backlinks_info": {
                  "se_type": "google",
                  "backlinks": 4502.4,
                  "dofollow": 2513.9,
                  "referring_pages": 3667.1,
                  "referring_domains": 984.5,
                  "referring_main_domains": 855.8,
                  "rank": 322.6,
                  "main_domain_rank": 814.6,
                  "last_updated_time": "2024-08-04 10:51:22 +00:00"
                },
                "search_intent_info": {
                  "se_type": "google",
                  "main_intent": "commercial",
                  "foreign_intent": [
                    "navigational"
                  ],
                  "last_updated_time": "2023-03-02 03:54:24 +00:00"
                },
                "keyword_info_normalized_with_bing": {
                  "last_updated_time": "2024-08-16 23:26:54 +00:00",
                  "search_volume": 4979,
                  "is_normalized": true,
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 4979
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 4979
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 4979
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 4979
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 4979
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 4979
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 4979
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 4979
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 4979
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 4979
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 4979
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 4979
                    }
                  ]
                },
                "keyword_info_normalized_with_clickstream": {
                  "last_updated_time": "2024-08-11 20:06:52 +00:00",
                  "search_volume": 22200,
                  "is_normalized": true,
                  "monthly_searches": [
                    {
                      "year": 2024,
                      "month": 7,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 6,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 5,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 4,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 3,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 2,
                      "search_volume": 22200
                    },
                    {
                      "year": 2024,
                      "month": 1,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 12,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 11,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 10,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 9,
                      "search_volume": 22200
                    },
                    {
                      "year": 2023,
                      "month": 8,
                      "search_volume": 22200
                    }
                  ]
                }
              },
              "depth": 1,
              "related_keywords": [
                "phone app download",
                "phone app on android",
                "my phone app",
                "phone app free",
                "google phone app",
                "phone call",
                "phone app download free",
                "phone by google"
              ]
            }
          ]
        }
      ]
    }
  ]
}

You can specify the number of results you want to retrieve, filter and sort them.

Below you will find a detailed description of the fields you can use for setting a task.

**Description of the fields for setting a task:**

| Field name | Type | Description |
| --- | --- | --- |
| `keyword` | string | _keyword_<br>**required field**<br>UTF-8 encoding<br>the keywords will be converted to lowercase format<br>learn more about rules and limitations of `keyword` and `keywords` fields in DataForSEO APIs in this [Help Center article](https://dataforseo.com/help-center/rules-and-limitations-of-keyword-and-keywords-fields-in-dataforseo-apis) |  |
| `location_name` | string | _full name of the location_<br>**required field if you don’t specify** `location_code`<br>**Note:** it is required to specify either `location_name` or `location_code`<br>you can receive the list of available locations with their `location_name` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`United Kingdom` |  |
| `location_code` | integer | _location code_<br>**required field if you don’t specify** `location_name`<br>**Note:** it is required to specify either `location_name` or `location_code`<br>you can receive the list of available locations with their `location_code` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`2840` |  |
| `language_name` | string | _full name of the language_<br>**required field if you don’t specify** `language_code`<br>**Note:** it is required to specify either `language_name` or `language_code`<br>you can receive the list of available locations with their `language_name` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`English` |  |
| `language_code` | string | _language code_<br>**required field if you don’t specify** `language_name`<br>**Note:** it is required to specify either `language_name` or `language_code`<br>you can receive the list of available locations with their `language_code` by making a separate request to the<br>`https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`<br>example:<br>`en` |  |
| `depth` | integer | _keyword search depth_<br>optional field<br>default value: `1` <br>number of the returned results depends on the value you set in this field<br>you can specify a level from 0 to 4<br>estimated number of keywords for each level (maximum):<br>0 – the keyword set in the `keyword` field<br>1 – 8 keywords<br>2 – 72 keywords<br>3 – 584 keywords<br>4 – 4680 keywords |  |
| `include_seed_keyword` | boolean | _include data for the seed keyword_<br>optional field<br>if set to `true`, data for the seed keyword specified in the `keyword` field will be provided in the `seed_keyword_data` array of the response<br>default value: `false` |  |
| `include_serp_info` | boolean | _include data from SERP for each keyword_<br>optional field<br>if set to `true`, we will return a `serp_info` array containing SERP data (number of search results, relevant URL, and SERP features) for every keyword in the response<br>default value: `false` |  |
| `include_clickstream_data` | boolean | _include or exclude data from clickstream-based metrics in the result_<br>optional field<br>if the parameter is set to `true`, you will receive `clickstream_keyword_info`, `keyword_info_normalized_with_clickstream`, and `keyword_info_normalized_with_bing` fields in the response<br>default value: `false`<br>with this parameter enabled, you will be charged double the price for the request<br>learn more about how clickstream-based metrics are calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `ignore_synonyms` | boolean | _ignore highly similar keywords_<br>optional field<br>if set to `true` only core keywords will be returned, all highly similar keywords will be excluded;<br>default value: `false` |  |
| `replace_with_core_keyword` | boolean | _return data for core keyword_<br>optional field<br>if `true`, `serp_info` and `related_keywords` will be returned for the main keyword in the group that the specified `keyword` belongs to;<br>if `false`, `serp_info` and `related_keywords` will be returned for the specified `keyword` (if available);<br>refer to [this help center article](https://dataforseo.com/help-center/replace_with_core_keyword) for more details;<br>default value: `false` |  |
| `filters` | array | _array of results filtering parameters_<br>optional field<br>**you can add several filters at once (8 filters maximum)**<br>you should set a logical operator `and`, `or` between the conditions<br>the following operators are supported:<br>`regex`, `not_regex`, `<`, `<=`, `>`, `>=`, `=`, `<>`, `in`, `not_in`, `match`, `not_match`, `ilike`, `not_ilike`, `like`, `not_like`<br>you can use the `%` operator with `like` and `not_like`, as well as `ilike` and `not_ilike` to match any string of zero or more characters<br>example:<br>`["keyword_data.keyword_info.search_volume",">",0]`<br>`[["keyword_info.search_volume","in",[0,1000]],<br>"and",<br>["keyword_data.keyword_info.competition_level","=","LOW"]]`<br>`[["keyword_data.keyword_info.search_volume",">",100],<br>"and",<br>[["keyword_data.keyword_info.cpc","<",0.5],<br>"or",<br>["keyword_info.high_top_of_page_bid","<=",0.5]]]`<br>for more information about filters, please refer to [Dataforseo Labs – Filters](https://docs.dataforseo.com/v3/dataforseo_labs/filters) or this [help center guide](https://dataforseo.com/help-center/how-to-use-filters-in-dataforseo-labs-api) |  |
| `order_by` | array | _results sorting rules_<br>optional field<br>you can use the same values as in the `filters` array to sort the results<br>possible sorting types:<br>`asc` – results will be sorted in the ascending order<br>`desc` – results will be sorted in the descending order<br>you should use a comma to set up a sorting type<br>example:<br>`["keyword_data.keyword_info.competition,desc"]`<br>default rule:<br>`["keyword_data.keyword_info.search_volume,desc"]`<br>**note that you can set no more than three sorting rules in a single request**<br>you should use a comma to separate several sorting rules<br>example:<br>`["keyword_data.keyword_info.search_volume,desc","keyword_data.keyword_info.cpc,desc"]` |  |
| `limit` | integer | _the maximum number of returned keywords_<br>optional field<br>default value: `100`<br>maximum value: `1000` |  |
| `offset` | integer | _offset in the results array of returned keywords_<br>optional field<br>default value: `0`<br>if you specify the `10` value, the first ten keywords in the results array will be omitted and the data will be provided for the successive keywords |  |
| `tag` | string | _user-defined task identifier_<br>optional field<br>_the character limit is 255_<br>you can use this parameter to identify the task and match it with the result<br>you will find the specified `tag` value in the `data` object of the response |  |

‌

As a response of the API server, you will receive [JSON](https://en.wikipedia.org/wiki/JSON)-encoded data containing a `tasks` array with the information specific to the set tasks.

**Description of the fields in the results array:**

| Field name | Type | Description |
| --- | --- | --- |
| `version` | string | _the current version of the API_ |  |
| `status_code` | integer | _general status code_<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors)<br>**Note:** we strongly recommend designing a necessary system for handling related exceptional or error conditions |  |
| `status_message` | string | _general informational message_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `time` | string | _execution time, seconds_ |  |
| `cost` | float | _total tasks cost, USD_ |  |
| `tasks_count` | integer | _the number of tasks in the **`tasks`** array_ |  |
| `tasks_error` | integer | _the number of tasks in the **`tasks`** array returned with an error_ |  |
| **`tasks`** | array | _array of tasks_ |  |
| `id` | string | _task identifier_<br>**unique task identifier in our system in the [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format** |  |
| `status_code` | integer | _status code of the task_<br>generated by DataForSEO; can be within the following range: 10000-60000<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `status_message` | string | _informational message of the task_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix-errors/) |  |
| `time` | string | _execution time, seconds_ |  |
| `cost` | float | _cost of the task, USD_ |  |
| `result_count` | integer | _number of elements in the `result` array_ |  |
| `path` | array | _URL path_ |  |
| `data` | object | _contains the same parameters that you specified in the POST request_ |  |
| **`result`** | array | _array of results_ |  |
| `se_type` | string | _search engine type_ |  |
| `seed_keyword` | string | _keyword in a POST array_ |  |
| **`seed_keyword_data`** | array | _keyword data for the seed keyword_<br>fields in the array are identical to that of `keyword_data` |  |
| `location_code` | integer | _location code in a POST array_ |  |
| `language_code` | string | _language code in a POST array_ |  |
| `total_count` | integer | _total amount of results in our database relevant to your request_ |  |
| `items_count` | integer | _the number of results returned in the `items` array_ |  |
| `items` | array | _contains keywords and related data_ |  |
| `se_type` | string | _search engine type_ |  |
| `keyword_data` | object | _keyword data for the returned keyword_ |  |
| `se_type` | string | _search engine type_ |  |
| `keyword` | string | _related keyword_ |  |
| `location_code` | integer | _location code in a POST array_ |  |
| `language_code` | string | _language code in a POST array_ |  |
| `keyword_info` | object | _keyword data for the returned keyword_ |  |
| `se_type` | string | _search engine type_ |  |
| `last_updated_time` | string | _date and time when keyword data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `competition` | float | _competition_<br>represents the relative amount of competition associated with the given keyword;<br>the value is based on Google Ads data and can be between 0 and 1 (inclusive) |  |
| `competition_level` | string | _competition level_<br>represents the relative level of competition associated with the given keyword in paid SERP only;<br>possible values: `LOW`, `MEDIUM`, `HIGH`<br>if competition level is unknown, the value is `null`;<br>learn more about the metric in [this help center article](https://dataforseo.com/help-center/what-is-competition) |  |
| `cpc` | float | _cost-per-click_<br>represents the average cost per click (USD) historically paid for the keyword |  |
| `search_volume` | integer | _average monthly search volume rate_<br>represents the (approximate) number of searches for the given keyword idea on google.com |  |
| `low_top_of_page_bid` | float | _minimum bid for the ad to be displayed at the top of the first page_<br>indicates the value greater than about 20% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)<br>the value may differ depending on the location specified in a POST request |  |
| `high_top_of_page_bid` | float | _maximum bid for the ad to be displayed at the top of the first page_<br>indicates the value greater than about 80% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers)<br>the value may differ depending on the location specified in a POST request |  |
| `categories` | array | _product and service categories_<br>you can download the [full list of possible categories](https://cdn.dataforseo.com/v3/categories/categories_dataforseo_labs_2023_10_25.csv) |  |
| `monthly_searches` | array | _monthly searches_<br>represents the (approximate) number of searches on this keyword idea (as available for the past twelve months), targeted to the specified geographic locations |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _monthly average search volume rate_ |  |
| `search_volume_trend` | object | _search volume trend changes_<br>represents search volume change in percent compared to the previous period |  |
| `monthly` | integer | _search volume change in percent compared to the previous month_ |  |
| `quarterly` | integer | _search volume change in percent compared to the previous quarter_ |  |
| `yearly` | integer | _search volume change in percent compared to the previous year_ |  |
| `clickstream_keyword_info` | object | _clickstream data for the returned keyword_<br>to retrieve results for this field, the parameter `include_clickstream_data` must be set to `true` |  |
| `search_volume` | integer | _monthly average clickstream search volume rate_ |  |
| `last_updated_time` | string | _date and time when the clickstream dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” |  |
| `gender_distribution` | object | _distribution of estimated clickstream-based metrics by gender_<br>learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `female` | integer | _number of female users in the relevant clickstream dataset_ |  |
| `male` | integer | _number of male users in the relevant clickstream dataset_ |  |
| `age_distribution` | object | _distribution of clickstream-based metrics by age_<br>learn more about how the metric is calculated in this [help center article](https://dataforseo.com/help-center/what-are-clickstream-based-metrics-and-how-do-we-calculate-them) |  |
| `18-24` | integer | _number of users in the relevant clickstream dataset that fall within the 18-24 age range_ |  |
| `25-34` | integer | _number of users in the relevant clickstream dataset that fall within the 25-34 age range_ |  |
| `35-44` | integer | _number of users in the relevant clickstream dataset that fall within the 35-44 age range_ |  |
| `45-54` | integer | _number of users in the relevant clickstream dataset that fall within the 45-54 age range_ |  |
| `55-64` | integer | _number of users in the relevant clickstream dataset that fall within the 55-64 age range_ |  |
| `monthly_searches` | array | _monthly clickstream search volume rates_<br>array of objects with clickstream search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _clickstream-based search volume rate in a certain month of a year_ |  |
| `keyword_properties` | object | _additional information about the keyword_ |  |
| `se_type` | string | _search engine type_ |  |
| `core_keyword` | string | _main keyword in a group_<br>contains the main keyword in a group determined by the synonym clustering algorithm<br>if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` |  |
| `synonym_clustering_algorithm` | string | _the algorithm used to identify synonyms_<br>possible values:<br>`keyword_metrics` – indicates the algorithm based on `keyword_info` parameters<br>`text_processing` – indicates the text-based algorithm<br>if the value is `null`, our database does not contain any keywords the corresponding algorithm could identify as synonymous with `keyword` |  |
| `keyword_difficulty` | integer | _difficulty of ranking in the first top-10 organic results for a keyword_<br>indicates the chance of getting in top-10 organic results for a keyword on a logarithmic scale from 0 to 100;<br>calculated by analysing, among other parameters, link profiles of the first 10 pages in SERP;<br>learn more about the metric in [this help center guide](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated) |  |
| `detected_language` | string | _detected language of the keyword_<br>indicates the language of the keyword as identified by our system |  |
| `is_another_language` | boolean | _detected language of the keyword is different from the set language_<br>if `true`, the language set in the request does not match the language determined by our system for a given keyword |  |
| `serp_info` | object | _SERP data_<br>the value will be `null` if you didn’t set the field `include_serp_info` to `true` in the POST array or if there is no SERP data for this keyword in our database |  |
| `se_type` | string | _search engine type_ |  |
| `check_url` | string | _direct URL to search engine results_<br>you can use it to make sure that we provided accurate results |  |
| `serp_item_types` | array | _types of search results in SERP_<br>contains types of search results (items) found in SERP<br>possible item types:<br>`answer_box`, `app`, `carousel`, `multi_carousel`, `featured_snippet`, `google_flights`, `google_reviews`, `third_party_reviews`, `google_posts`, `images`, `jobs`, `knowledge_graph`, `local_pack`, `hotels_pack`, `map`, `organic`, `paid`, `people_also_ask`, `related_searches`, `people_also_search`, `shopping`, `top_stories`, `twitter`, `video`, `events`, `mention_carousel`, `recipes`, `top_sights`, `scholarly_articles`, `popular_products`, `podcasts`, `questions_and_answers`, `find_results_on`, `stocks_box`, `visual_stories`, `commercial_units`, `local_services`, `google_hotels`, `math_solver`, `currency_box`, `product_considerations`, `found_on_web`, `short_videos`, `refine_products`, `explore_brands`, `perspectives`, `discussions_and_forums`, `compare_sites`, `courses`, `ai_overview`;<br>**note** that the actual results will be returned only for `organic`, `paid`, `featured_snippet`, and `local_pack` elements |  |
| `se_results_count` | integer | _number of search results for the returned keyword_ |  |
| `last_updated_time` | string | _date and time when SERP data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `previous_updated_time` | string | _previous to the most recent date and time when SERP data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-10-15 12:57:46 +00:00` |  |
| `avg_backlinks_info` | object | _backlink data for the returned keyword_<br>this object provides the average number of backlinks, referring pages and domains, as well as the average rank values among the top-10 webpages ranking organically for the keyword |  |
| `se_type` | string | _search engine type_ |  |
| `backlinks` | float | _average number of backlinks_ |  |
| `dofollow` | float | _average number of dofollow links_ |  |
| `referring_pages` | float | _average number of referring pages_ |  |
| `referring_domains` | float | _average number of referring domains_ |  |
| `referring_main_domains` | float | _average number of referring main domains_ |  |
| `rank` | float | _average rank_<br>learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) |  |
| `main_domain_rank` | float | _average main domain rank_<br>learn more about the metric and its calculation formula in [this help center article](https://dataforseo.com/help-center/what_is_rank_in_backlinks_api) |  |
| `last_updated_time` | string | _date and time when backlink data was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `search_intent_info` | object | _search intent info for the returned keyword_<br>learn about search intent in this [help center article](https://dataforseo.com/help-center/search-intent-and-its-types) |  |
| `se_type` | string | _search engine type_<br>possible values: `google` |  |
| `main_intent` | string | _main search intent_<br>possible values: `informational`, `navigational`, `commercial`, `transactional` |  |
| `foreign_intent` | array | _supplementary search intents_<br>possible values: `informational`, `navigational`, `commercial`, `transactional` |  |
| `last_updated_time` | string | _date and time when search intent data was last updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| **`keyword_info_normalized_with_bing`** | object | _contains keyword search volume normalized with Bing search volume_ |  |
| `last_updated_time` | string | _date and time when the dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `search_volume` | integer | _current search volume rate of a keyword_ |  |
| `is_normalized` | boolean | _keyword info is normalized_<br>if `true`, values are normalized with Bing data |  |
| `monthly_searches` | integer | _monthly search volume rates_<br>array of objects with search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _search volume rate in a certain month of a year_ |  |
| **`keyword_info_normalized_with_clickstream`** | object | _contains keyword search volume normalized with clickstream data_ |  |
| `last_updated_time` | string | _date and time when the dataset was updated_<br>in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2019-11-15 12:57:46 +00:00` |  |
| `search_volume` | integer | _current search volume rate of a keyword_ |  |
| `is_normalized` | boolean | _keyword info is normalized_<br>if `true`, values are normalized with clickstream data |  |
| `monthly_searches` | integer | _monthly search volume rates_<br>array of objects with search volume rates in a certain month of a year |  |
| `year` | integer | _year_ |  |
| `month` | integer | _month_ |  |
| `search_volume` | integer | _search volume rate in a certain month of a year_ |  |
| `depth` | integer | _keyword search depth_ |  |
| `related_keywords` | array | _list of related keywords_<br>represents the list of search queries which are related to the keyword returned in the array above |  |

‌‌
FILTERS:

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

          "related_keywords": {
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


## Filters for DataForSEO Labs API

‌‌

Here you will find all the necessary information about filters that can be used with DataForSEO Labs API endpoints.

Please, keep in mind that filters are associated with a certain object in the `result` array, and should be specified accordingly.

We recommend learning more about how to use filters in [this Help Center article](https://dataforseo.com/help-center/using-filters).

**Note that it is not possible to use the following types of fields as sorting rules in `order_by`: `array.str`, `array.num`.**





You will receive the full list of filters by calling this API. You can also download the full list of possible filters [by this link.](https://cdn.dataforseo.com/v3/available_filters.php?api=dataforseo_labs)

‌‌As a response of the API server, you will receive [JSON](https://en.wikipedia.org/wiki/JSON)-encoded data containing a `tasks` array with the information specific to the set tasks.

| Field name | Type | Description |
| --- | --- | --- |
| `version` | string | _the current version of the API_ |  |
| `status_code` | integer | _general status code_<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `status_message` | string | _general informational message_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `time` | string | _execution time, seconds_ |  |
| `cost` | float | _total tasks cost, USD_ |  |
| `tasks_count` | integer | _the number of tasks in the **`tasks`** array_ |  |
| `tasks_error` | integer | _the number of tasks in the **`tasks`** array returned with an error_ |  |
| **`tasks`** | array | _array of tasks_ |  |
| `id` | string | _task identifier_<br>**unique task identifier in our system in the [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format** |  |
| `status_code` | integer | _status code of the task_<br>generated by DataForSEO; can be within the following range: 10000-60000<br>you can find the full list of the response codes [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `status_message` | string | _informational message of the task_<br>you can find the full list of general informational messages [here](https://docs.dataforseo.com/v3/appendix/errors) |  |
| `time` | string | _execution time, seconds_ |  |
| `cost` | float | _cost of the task, USD_ |  |
| `result_count` | integer | _number of elements in the `result` array_ |  |
| `path` | array | _URL path_ |  |
| `data` | object | _contains the parameters passed in the URL of the GET request_ |  |
| **`result`** | array | _array of results_<br>contains the full list of available parameters that can be used for data filtration<br>the parameters are grouped by the endpoint they can be used with |  |

Below you will find a detailed description of the structure that should be used to specify `filters` when setting tasks with DataForSEO Labs API. You will also find the types of parameters that can be used with each endpoint, and examples of pre-made filters.

**Description of the fields:**

| Field name | Type | Description |
| --- | --- | --- |
| `filters` | array | _array of results filtering parameters_<br>optional field<br>**you can add several filters at once (8 filters maximum)**<br>you should set a logical operator `and`, `or` between the conditions<br>filters have the following structure:<br>`[` `$item_array` `.` `$results_array` `.` `$parameter_field` `,` `$filter_operator` `,` `$filter_value` `]`<br>you should use the `.` and `,` symbols as separators<br>example:<br>`["keyword_data.keyword_info.search_volume", ">=", 50]` <br>Page Intersection, Ranked Keywords, Subdomains, Relevant Pages, Competitors Domain, Categories For Domain, Domain Intersection endpoints also support an alternative structure:<br>`[` `$item_array` `.` `$results_array` `.` `$parameter_field` `,` `$filter_operator` `,` `$item->` `$item_array` `.` `$results_array` `.` `$parameter_field` `]`<br>if you use this structure, you need to attach `$item->` to the right part of the condition<br>**note** that the `$parameter_field` variables in the right part and in the left part of the condition should have identical type: `bool`, `num`, `str`, `time`<br>example:<br>`["metrics.organic.pos_1", ">", "$item->metrics.organic.pos_2_3"]` |  |
| `$item_array` | str | _item name in the filter_<br>optional field<br>possible values:<br>`keyword_data`, `ranked_serp_element` |  |
| `$results_array` | str | _results array in the filter_<br>optional field<br>possible values:<br>`keyword`, `keyword_info`, `check_url`, `se_results_count`, `serp_item`, `metrics` |  |
| `$parameter_field` | str | _parameter field in the filter_<br>optional field<br>**required field if the filter is applied**<br>the parameter in the superordinate `$results_array` or `item_array`<br>represents the field you want to filter the results by |  |
| `$filter_operator` | str | _operator in the filter_<br>optional field<br>**required field if the filter is applied**<br>available filter operators:<br>• if **`bool`**: `=`, `<>`<br>• if **`num`**: `<`, `<=`, `>`, `>=`, `=`, `<>`, `in`, `not_in`<br>• if **`str`**: `match`, `not_match`, `like`, `not_like`, `ilike`, `not_ilike`, `in`, `not_in`, `=`, `<>`, `regex`, `not_regex`<br>• if **`array.str`**: `has`, `has_not`<br>• if **`array.num`**: `has`, `has_not`<br>• if **`time`**: `<`, `>` <br>note: `time` should be specified in the format: “yyyy-mm-dd hh-mm-ss +00:00”<br>example:<br>`2021-01-29 15:02:37 +00:00`<br>if you specify `in` or `not_in` operator, the `$filter_value` should be specified as an array<br>example:<br>`["keyword_info.search_volume","in",[10,1000]]`<br>`regex` and `not_regex` operators can be specified with `string` values using the [RE2 regex](https://github.com/google/re2/wiki/Syntax) syntax;<br>**Note:** the maximum limit for the number of characters you can specify in `regex` and `not_regex` is **1000**;<br>example:<br>string contains keywords: ` ["keyword_data.keyword", "regex", "(how|what|when)"]`<br>string does not contain keywords: ` ["keyword_data.keyword", "not_regex", "(how|what|when)"]`<br>`like` and `not_like` operators require adding `%` symbol to get accurate results<br>example:<br>`["keyword_data.keyword", "like", "%seo%"]` return `keyword_data` items that contain “seo” in the `keyword` field<br>`["keyword_data.keyword", "not_like", "%seo%"]` do not return `keyword_data` items that contain “seo” in the `keyword` field<br>`match` and `not_match` are full-text search operators that work with `string` values<br>example:<br>`["keyword", "not_match", "camera"]` return keywords that do not contain the “camera” word<br>`["keyword", "match", "phone"]` return keywords that contain the “phone” word |  |
| `$filter_value` | num<br>str<br>bool<br>time | _filtering value_<br>optional field<br>**required field if the filter is applied** |  |

# Using filters in DataForSEO APIs


With DataForSEO APIs, you can get very specific in your research, competitor analysis, and market study. By using the filters available for our APIs, you will always get the most relevant data in the response, which will enable you to reduce the number of requests and save your budget accordingly.


**_You can set a maximum of eight filters in a single API request._**

Filters are associated with certain parameters from the API response. Each endpoint provides different data, and thus the filter structure and values differ depending on the endpoint.

Generally the structure of the filter includes three parts that are separated with a `,` symbol:

- filtered parameter – target parameter of the endpoint you want to filter;
- filter operator – operator of the filter;
- filter value – filtering value.

You can find the exact filter structure in the description of each DataForSEO API below.

In addition, filters support different data types. If you look at the list of supported filters, you will find the supported data type after the colon in each filter.

For example, `"keyword_info.search_volume": "num"` where `num` is the supported data type.

Each data type, in turn, supports different filter operators.

> For example, for the ["main_domain": "str"] filter, we can use one of the following operators: `match`, `not_match`, `like`, `not_like`, `ilike`, `not_ilike`, `=`, `<>`.

### How to use operators?

1When you use the `in` or **`not_in`** operator, the filter value should be specified as an array.

_Example:_ `["keyword_info.search_volume","in",[10,1000]]`

2The **`like`** and **`not_like`** operators require adding the `%` symbol to get accurate results.

_Example:_

The `["keyword_data.keyword", "like", "%seo%"]` filter returns `keyword_data` items that contain “seo” anywhere in the keyword string and the `["keyword_data.keyword", "not_like", "%seo%"]` filter returns `keyword_data` items that don’t contain “seo” anywhere in the keyword string.

3The **`match`** and **`not_match`** are full-text search operators that only work with `string` values.

_Example:_

The `["keyword", "match", "phone"]` will return data for keywords that contain the “phone” word anywhere in the string.

4As for the **`has`** and `has_not` operators, they can be used only for `array.str` and `array.num`.

For example, the `serp_item_types` parameter in the [Keyword Suggestions endpoint](https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live/?bash) is the array of strings that displays SERP features available for the specified keyword ( `featured_snippet`, `answer_box`, `knowledge_graph`, and others).

By applying a filter with the `has` or `has_not` operator to this parameter, you can receive the keywords for which a certain element is present or not present in SERP.

_Example:_

`["serp_info.serp_item_types", "has", "featured_snippet"]`

In this case, the API response will return only the keywords that have featured snippets in SERP.

And after the filter operator comes the filtering value, which may take the form of a string, array string, number, or boolean.

_**To not get confused with filter structure, we recommend calling the Available Filters endpoint and checking the examples.**_

### Using Regex Operator

The `regex` operator is supported in DataForSEO Labs API, OnPage API, Backlinks API, Content Analysis API and works only with `string` values.

**Note:** the maximum number of symbols you can specify in `regex` and `not_regex` is 1000;

**`.`** – Matches any character. For example:

`ab.` # matches ‘aba’, ‘abb’, ‘abz’, etc.

**`?`** – Repeat the preceding character zero or one times. Often used to make the preceding character optional. For example:

`abc?` # matches ‘ab’ and ‘abc’

**`+`** – Repeat the preceding character one or more times. For example:

`ab+` # matches ‘ab’, ‘abb’, ‘abbb’, etc.

**`*`** – Repeat the preceding character zero or more times. For example:

`ab*` # matches ‘a’, ‘ab’, ‘abb’, ‘abbb’, etc.

**`{}`** – Minimum and maximum number of times the preceding character can repeat. For example:

`a{2}` # matches ‘aa’

`a{2,4}` # matches ‘aa’, ‘aaa’, and ‘aaaa’

`a{2,}` # matches ‘a\` repeated two or more times

**`|`** – OR operator. The match will succeed if the longest pattern on either the left side OR the right side matches. For example:

`abc|xyz` # matches ‘abc’ and ‘xyz’

**`( … )`** – Forms a group. You can use a group to treat part of the expression as a single character. For example:

abc(def)? # matches ‘abc’ and ‘abcdef’ but not ‘abcd’

**`[ … ]`** – Match one of the characters in the brackets. For example:

`[abc]` # matches ‘a’, ‘b’, ‘c’

Inside the brackets, `-` indicates a range unless – is the first character or escaped. For example:

`[a-c]` # matches ‘a’, ‘b’, or ‘c’

`[-abc]` # ‘-‘ is first character. Matches ‘-‘, ‘a’, ‘b’, or ‘c’

`[abc\-]` # Escapes ‘-‘. Matches ‘a’, ‘b’, ‘c’, or ‘-‘

A `^` before a character in the brackets negates the character or range. For example:

`[^abc]` # matches any character except ‘a’, ‘b’, or ‘c’

`[^a-c]` # matches any character except ‘a’, ‘b’, or ‘c’

`[^-abc]` # matches any character except ‘-‘, ‘a’, ‘b’, or ‘c’

`[^abc\-]` # matches any character except ‘a’, ‘b’, ‘c’, or ‘-‘

**Note:** backslash symbols ( `"\"`) in DataForSEO Regex can have different interpretations:

- `\b` is interpreted as a backspace symbol (not the same as in standard regex);
- `\\b` asserts that the current position in the string is a word boundary (same as `"\b"` in standard regex);
- `\\\\b` means 2 separate signs: `"\"` and `"b"` (for example, if you need to find `"a\b"` – you’d have to pass it as `"\\\\b"`;

If you specify `"\\"` without the expected symbol after it (for example `\\c` instead of `\\\\` or `\\c`), API will return a 4xx error.

APIs with filtration parameters also support the negative regex operator called `not_regex`, which allows for the exclusion of a certain string from API results.

_Example:_

Return string that contains “how”, “what”, or “when” keywords: `["keyword_data.keyword", "regex", "(how|what|when)"]`

Return string that does not contain “how”, “what”, or “when” keywords: `["keyword_data.keyword", "not_regex", "(how|what|when)"]`

You can test parameters with regex operator [via this link](https://regex101.com/).

The tool utilizes APIs from **DataForSEO** (for discovery, SERP analysis, and competitor checks), **OpenAI** (for AI analysis and content generation), and **Pexels** (for image retrieval). The costs associated with these endpoints are detailed below, drawn directly from the provided documentation.

## 1. DataForSEO API Costs

DataForSEO charges are structured per task or per item (keyword/page crawled), often with multipliers for specialized data inclusion. The system reports the total cost for all tasks (`total tasks cost, USD`) and the cost of the individual task (`cost of the task, USD`).

### A. Discovery Endpoints (DataForSEO Labs Google API)

The tool utilizes Keyword Ideas, Keyword Suggestions, and Related Keywords endpoints. These are categorized under "All Other Endpoints" unless specified otherwise, and operate in **Live mode** with a turnaround time of up to **2 seconds** on average.

| Endpoint Category | Cost Per Task | Cost Per Item (Keyword/Domain) | Example Calculation | Source |
| :--- | :--- | :--- | :--- | :--- |
| **All Other Endpoints** | **\$0.01** | **\$0.0001** | $110 for 1M keywords/domains | |
| **Search Intent** | **\$0.001** | **\$0.0001** | $101 for 1M keywords | |

**Key Cost Multiplier:**

| Parameter | Cost Impact | Source |
| :--- | :--- | :--- |
| **`include_clickstream_data`** | If set to `true`, **the cost of the request is multiplied by 2**. | |

### B. SERP Endpoint (`serp/google/organic/live/advanced`)

The Live Mode is used, featuring an accelerated turnaround time (up to **6 seconds** on average). The cost is based on the number of requested SERPs (with 10 search results each).

| Component | Live Mode Price | Additional Charges / Notes | Source |
| :--- | :--- | :--- | :--- |
| **Price per 1 SERP** (10 results) | **\$0.002** | Base rate for the first SERP page. | |
| **Subsequent SERP Pages** | **75% of the base rate** | Charged per results page requested after the first. | |
| **Max Crawl Pages / Depth** | You will be **charged for each page crawled** (10 organic results per page). Setting depth above 10 may result in additional charges if the search engine returns more than 10 results. | |
| **`calculate_rectangles`** | **Extra \$0.002**. | Charged for calculating pixel rankings. | |
| **`load_async_ai_overview`** | **Extra \$0.002**. | Charged to obtain AI overview items asynchronously. | |
| **`people_also_ask_click_depth`** | **\$0.00015 extra for each click**. | | |
| **Keyword Operators** | **Multiply by 5 for each parameter used**. | Applies if the `keyword` field contains advanced search parameters like *‘site:’* or *‘allinurl:’*. | |

### C. OnPage Endpoint (`on_page/instant_pages`)

The account is **charged for each request made to this endpoint**. The price calculation is based on the **Basic price** of **\$0.000125 per crawled page**.

| Parameter / Feature | Price Per Crawled Page (Additive) | Calculation (where $P = \$0.000125$) | Source |
| :--- | :--- | :--- | :--- |
| **Basic / Instant Pages** | **\$0.000125** | $P$ | |
| **Load Resources** (`load_resources`) | **\$0.000375** | $P + P \times 2$ | |
| **Enable JavaScript** (`enable_javascript`) | **\$0.00125** | $P + P \times 9$ | |
| **Custom JavaScript** (`custom_js`) | **\$0.00025** | $P + P$ | |
| **Calculate Keyword Density** | **\$0.00025** | $P + P$ | |
| **Enable Browser Rendering** | **\$0.00425** | $P + P \times 33$ | |
| **Page Screenshot** | **\$0.0040** | N/A | |
| **Enable Content Parsing** | **\$0.000125 per parsed page** | N/A | |

**Note:** If `enable_browser_rendering` is used, `enable_javascript` and `load_resources` are enabled automatically, and **additional charges will apply**.

## 2. OpenAI API Costs (LLM)

OpenAI costs are calculated based on the tokens consumed (`prompt_tokens` and `completion_tokens`) using specific pricing tiers for each model.

**OpenAI Model Pricing (Per 1 Million Tokens)**

| Model Name | Input Price (per 1M tokens) | Output Price (per 1M tokens) | Source |
| :--- | :--- | :--- | :--- |
| **`gpt-4o`** | **\$5.00** | **\$15.00** | |
| **`gpt-4-turbo`** | **\$10.00** | **\$30.00** | |
| **`gpt-3.5-turbo`**| **\$0.50** | **\$1.50** | |

The tool's orchestrator uses **hardcoded approximations** for cost estimation, which are often based on the `gpt-4o` model:

*   **Analyze Action:** Estimated cost includes a fixed $\sim\text{\$0.05}$ for the OpenAI analysis call.
*   **Generate Action:** Estimated cost includes $\sim\text{\$0.15}$ for the full article generation call and $\sim\text{\$0.02}$ for the social media posts call.

## 3. Pexels API Costs

The Pexels API is used for image search. Pexels provides photos and videos **free of charge**. The internal `PexelsClient` reflects this by returning a cost of **0.0**.

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


Structured model outputs
========================

Ensure text responses from the model adhere to a JSON schema you define.

JSON is one of the most widely used formats in the world for applications to exchange data.

Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied [JSON Schema](https://json-schema.org/overview/what-is-jsonschema), so you don't need to worry about the model omitting a required key, or hallucinating an invalid enum value.

Some benefits of Structured Outputs include:

1.  **Reliable type-safety:** No need to validate or retry incorrectly formatted responses
2.  **Explicit refusals:** Safety-based model refusals are now programmatically detectable
3.  **Simpler prompting:** No need for strongly worded prompts to achieve consistent formatting

In addition to supporting JSON Schema in the REST API, the OpenAI SDKs for [Python](https://github.com/openai/openai-python/blob/main/helpers.md#structured-outputs-parsing-helpers) and [JavaScript](https://github.com/openai/openai-node/blob/master/helpers.md#structured-outputs-parsing-helpers) also make it easy to define object schemas using [Pydantic](https://docs.pydantic.dev/latest/) and [Zod](https://zod.dev/) respectively. Below, you can see how to extract information from unstructured text that conforms to a schema defined in code.

Getting a structured response

```javascript
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const response = await openai.responses.parse({
  model: "gpt-4o-2024-08-06",
  input: [
    { role: "system", content: "Extract the event information." },
    {
      role: "user",
      content: "Alice and Bob are going to a science fair on Friday.",
    },
  ],
  text: {
    format: zodTextFormat(CalendarEvent, "event"),
  },
});

const event = response.output_parsed;
```

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

event = response.output_parsed
```

### Supported models

Structured Outputs is available in our [latest large language models](/docs/models), starting with GPT-4o. Older models like `gpt-4-turbo` and earlier may use [JSON mode](/docs/guides/structured-outputs#json-mode) instead.

When to use Structured Outputs via function calling vs via text.format

--------------------------------------------------------------------------

Structured Outputs is available in two forms in the OpenAI API:

1.  When using [function calling](/docs/guides/function-calling)
2.  When using a `json_schema` response format

Function calling is useful when you are building an application that bridges the models and functionality of your application.

For example, you can give the model access to functions that query a database in order to build an AI assistant that can help users with their orders, or functions that can interact with the UI.

Conversely, Structured Outputs via `response_format` are more suitable when you want to indicate a structured schema for use when the model responds to the user, rather than when the model calls a tool.

For example, if you are building a math tutoring application, you might want the assistant to respond to your user using a specific JSON Schema so that you can generate a UI that displays different parts of the model's output in distinct ways.

Put simply:

*   If you are connecting the model to tools, functions, data, etc. in your system, then you should use function calling - If you want to structure the model's output when it responds to the user, then you should use a structured `text.format`

The remainder of this guide will focus on non-function calling use cases in the Responses API. To learn more about how to use Structured Outputs with function calling, check out the

[

Function Calling

](/docs/guides/function-calling#function-calling-with-structured-outputs)

guide.

### Structured Outputs vs JSON mode

Structured Outputs is the evolution of [JSON mode](/docs/guides/structured-outputs#json-mode). While both ensure valid JSON is produced, only Structured Outputs ensure schema adherence. Both Structured Outputs and JSON mode are supported in the Responses API, Chat Completions API, Assistants API, Fine-tuning API and Batch API.

We recommend always using Structured Outputs instead of JSON mode when possible.

However, Structured Outputs with `response_format: {type: "json_schema", ...}` is only supported with the `gpt-4o-mini`, `gpt-4o-mini-2024-07-18`, and `gpt-4o-2024-08-06` model snapshots and later.

||Structured Outputs|JSON Mode|
|---|---|---|
|Outputs valid JSON|Yes|Yes|
|Adheres to schema|Yes (see supported schemas)|No|
|Compatible models|gpt-4o-mini, gpt-4o-2024-08-06, and later|gpt-3.5-turbo, gpt-4-* and gpt-4o-* models|
|Enabling|text: { format: { type: "json_schema", "strict": true, "schema": ... } }|text: { format: { type: "json_object" } }|

Examples
--------

Chain of thought

### Chain of thought

You can ask the model to output an answer in a structured, step-by-step way, to guide the user through the solution.

Structured Outputs for chain-of-thought math tutoring

```javascript
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const Step = z.object({
  explanation: z.string(),
  output: z.string(),
});

const MathReasoning = z.object({
  steps: z.array(Step),
  final_answer: z.string(),
});

const response = await openai.responses.parse({
  model: "gpt-4o-2024-08-06",
  input: [
    {
      role: "system",
      content:
        "You are a helpful math tutor. Guide the user through the solution step by step.",
    },
    { role: "user", content: "how can I solve 8x + 7 = -23" },
  ],
  text: {
    format: zodTextFormat(MathReasoning, "math_reasoning"),
  },
});

const math_reasoning = response.output_parsed;
```

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
        },
        {"role": "user", "content": "how can I solve 8x + 7 = -23"},
    ],
    text_format=MathReasoning,
)

math_reasoning = response.output_parsed
```

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-2024-08-06",
    "input": [
      {
        "role": "system",
        "content": "You are a helpful math tutor. Guide the user through the solution step by step."
      },
      {
        "role": "user",
        "content": "how can I solve 8x + 7 = -23"
      }
    ],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "math_reasoning",
        "schema": {
          "type": "object",
          "properties": {
            "steps": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "explanation": { "type": "string" },
                  "output": { "type": "string" }
                },
                "required": ["explanation", "output"],
                "additionalProperties": false
              }
            },
            "final_answer": { "type": "string" }
          },
          "required": ["steps", "final_answer"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  }'
```

#### Example response

```json
{
  "steps": [
    {
      "explanation": "Start with the equation 8x + 7 = -23.",
      "output": "8x + 7 = -23"
    },
    {
      "explanation": "Subtract 7 from both sides to isolate the term with the variable.",
      "output": "8x = -23 - 7"
    },
    {
      "explanation": "Simplify the right side of the equation.",
      "output": "8x = -30"
    },
    {
      "explanation": "Divide both sides by 8 to solve for x.",
      "output": "x = -30 / 8"
    },
    {
      "explanation": "Simplify the fraction.",
      "output": "x = -15 / 4"
    }
  ],
  "final_answer": "x = -15 / 4"
}
```

Structured data extraction

### Structured data extraction

You can define structured fields to extract from unstructured input data, such as research papers.

Extracting data from research papers using Structured Outputs

```javascript
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const ResearchPaperExtraction = z.object({
  title: z.string(),
  authors: z.array(z.string()),
  abstract: z.string(),
  keywords: z.array(z.string()),
});

const response = await openai.responses.parse({
  model: "gpt-4o-2024-08-06",
  input: [
    {
      role: "system",
      content:
        "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure.",
    },
    { role: "user", content: "..." },
  ],
  text: {
    format: zodTextFormat(ResearchPaperExtraction, "research_paper_extraction"),
  },
});

const research_paper = response.output_parsed;
```

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure.",
        },
        {"role": "user", "content": "..."},
    ],
    text_format=ResearchPaperExtraction,
)

research_paper = response.output_parsed
```

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-2024-08-06",
    "input": [
      {
        "role": "system",
        "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."
      },
      {
        "role": "user",
        "content": "..."
      }
    ],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "research_paper_extraction",
        "schema": {
          "type": "object",
          "properties": {
            "title": { "type": "string" },
            "authors": {
              "type": "array",
              "items": { "type": "string" }
            },
            "abstract": { "type": "string" },
            "keywords": {
              "type": "array",
              "items": { "type": "string" }
            }
          },
          "required": ["title", "authors", "abstract", "keywords"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  }'
```

#### Example response

```json
{
  "title": "Application of Quantum Algorithms in Interstellar Navigation: A New Frontier",
  "authors": [
    "Dr. Stella Voyager",
    "Dr. Nova Star",
    "Dr. Lyra Hunter"
  ],
  "abstract": "This paper investigates the utilization of quantum algorithms to improve interstellar navigation systems. By leveraging quantum superposition and entanglement, our proposed navigation system can calculate optimal travel paths through space-time anomalies more efficiently than classical methods. Experimental simulations suggest a significant reduction in travel time and fuel consumption for interstellar missions.",
  "keywords": [
    "Quantum algorithms",
    "interstellar navigation",
    "space-time anomalies",
    "quantum superposition",
    "quantum entanglement",
    "space travel"
  ]
}
```

UI generation

### UI Generation

You can generate valid HTML by representing it as recursive data structures with constraints, like enums.

Generating HTML using Structured Outputs

```javascript
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const UI = z.lazy(() =>
  z.object({
    type: z.enum(["div", "button", "header", "section", "field", "form"]),
    label: z.string(),
    children: z.array(UI),
    attributes: z.array(
      z.object({
        name: z.string(),
        value: z.string(),
      })
    ),
  })
);

const response = await openai.responses.parse({
  model: "gpt-4o-2024-08-06",
  input: [
    {
      role: "system",
      content: "You are a UI generator AI. Convert the user input into a UI.",
    },
    {
      role: "user",
      content: "Make a User Profile Form",
    },
  ],
  text: {
    format: zodTextFormat(UI, "ui"),
  },
});

const ui = response.output_parsed;
```

```python
from enum import Enum
from typing import List

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class UIType(str, Enum):
    div = "div"
    button = "button"
    header = "header"
    section = "section"
    field = "field"
    form = "form"

class Attribute(BaseModel):
    name: str
    value: str

class UI(BaseModel):
    type: UIType
    label: str
    children: List["UI"]
    attributes: List[Attribute]

UI.model_rebuild()  # This is required to enable recursive types

class Response(BaseModel):
    ui: UI

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "You are a UI generator AI. Convert the user input into a UI.",
        },
        {"role": "user", "content": "Make a User Profile Form"},
    ],
    text_format=Response,
)

ui = response.output_parsed
```

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-2024-08-06",
    "input": [
      {
        "role": "system",
        "content": "You are a UI generator AI. Convert the user input into a UI."
      },
      {
        "role": "user",
        "content": "Make a User Profile Form"
      }
    ],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "ui",
        "description": "Dynamically generated UI",
        "schema": {
          "type": "object",
          "properties": {
            "type": {
              "type": "string",
              "description": "The type of the UI component",
              "enum": ["div", "button", "header", "section", "field", "form"]
            },
            "label": {
              "type": "string",
              "description": "The label of the UI component, used for buttons or form fields"
            },
            "children": {
              "type": "array",
              "description": "Nested UI components",
              "items": {"$ref": "#"}
            },
            "attributes": {
              "type": "array",
              "description": "Arbitrary attributes for the UI component, suitable for any element",
              "items": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "The name of the attribute, for example onClick or className"
                  },
                  "value": {
                    "type": "string",
                    "description": "The value of the attribute"
                  }
                },
                "required": ["name", "value"],
                "additionalProperties": false
              }
            }
          },
          "required": ["type", "label", "children", "attributes"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  }'
```

#### Example response

```json
{
  "type": "form",
  "label": "User Profile Form",
  "children": [
    {
      "type": "div",
      "label": "",
      "children": [
        {
          "type": "field",
          "label": "First Name",
          "children": [],
          "attributes": [
            {
              "name": "type",
              "value": "text"
            },
            {
              "name": "name",
              "value": "firstName"
            },
            {
              "name": "placeholder",
              "value": "Enter your first name"
            }
          ]
        },
        {
          "type": "field",
          "label": "Last Name",
          "children": [],
          "attributes": [
            {
              "name": "type",
              "value": "text"
            },
            {
              "name": "name",
              "value": "lastName"
            },
            {
              "name": "placeholder",
              "value": "Enter your last name"
            }
          ]
        }
      ],
      "attributes": []
    },
    {
      "type": "button",
      "label": "Submit",
      "children": [],
      "attributes": [
        {
          "name": "type",
          "value": "submit"
        }
      ]
    }
  ],
  "attributes": [
    {
      "name": "method",
      "value": "post"
    },
    {
      "name": "action",
      "value": "/submit-profile"
    }
  ]
}
```

Moderation

### Moderation

You can classify inputs on multiple categories, which is a common way of doing moderation.

Moderation using Structured Outputs

```javascript
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const ContentCompliance = z.object({
  is_violating: z.boolean(),
  category: z.enum(["violence", "sexual", "self_harm"]).nullable(),
  explanation_if_violating: z.string().nullable(),
});

const response = await openai.responses.parse({
    model: "gpt-4o-2024-08-06",
    input: [
      {
        "role": "system",
        "content": "Determine if the user input violates specific guidelines and explain if they do."
      },
      {
        "role": "user",
        "content": "How do I prepare for a job interview?"
      }
    ],
    text: {
        format: zodTextFormat(ContentCompliance, "content_compliance"),
    },
});

const compliance = response.output_parsed;
```

```python
from enum import Enum
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class Category(str, Enum):
    violence = "violence"
    sexual = "sexual"
    self_harm = "self_harm"

class ContentCompliance(BaseModel):
    is_violating: bool
    category: Optional[Category]
    explanation_if_violating: Optional[str]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "Determine if the user input violates specific guidelines and explain if they do.",
        },
        {"role": "user", "content": "How do I prepare for a job interview?"},
    ],
    text_format=ContentCompliance,
)

compliance = response.output_parsed
```

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-2024-08-06",
    "input": [
      {
        "role": "system",
        "content": "Determine if the user input violates specific guidelines and explain if they do."
      },
      {
        "role": "user",
        "content": "How do I prepare for a job interview?"
      }
    ],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "content_compliance",
        "description": "Determines if content is violating specific moderation rules",
        "schema": {
          "type": "object",
          "properties": {
            "is_violating": {
              "type": "boolean",
              "description": "Indicates if the content is violating guidelines"
            },
            "category": {
              "type": ["string", "null"],
              "description": "Type of violation, if the content is violating guidelines. Null otherwise.",
              "enum": ["violence", "sexual", "self_harm"]
            },
            "explanation_if_violating": {
              "type": ["string", "null"],
              "description": "Explanation of why the content is violating"
            }
          },
          "required": ["is_violating", "category", "explanation_if_violating"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  }'
```

#### Example response

```json
{
  "is_violating": false,
  "category": null,
  "explanation_if_violating": null
}
```

How to use Structured Outputs with text.format
----------------------------------------------

Step 1: Define your schema

First you must design the JSON Schema that the model should be constrained to follow. See the [examples](/docs/guides/structured-outputs#examples) at the top of this guide for reference.

While Structured Outputs supports much of JSON Schema, some features are unavailable either for performance or technical reasons. See [here](/docs/guides/structured-outputs#supported-schemas) for more details.

#### Tips for your JSON Schema

To maximize the quality of model generations, we recommend the following:

*   Name keys clearly and intuitively
*   Create clear titles and descriptions for important keys in your structure
*   Create and use evals to determine the structure that works best for your use case

Step 2: Supply your schema in the API call

To use Structured Outputs, simply specify

```json
text: { format: { type: "json_schema", "strict": true, "schema": … } }
```

For example:

```python
response = client.responses.create(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"}
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "math_response",
            "schema": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": {"type": "string"},
                                "output": {"type": "string"}
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": False
                        }
                    },
                    "final_answer": {"type": "string"}
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

print(response.output_text)
```

```javascript
const response = await openai.responses.create({
    model: "gpt-4o-2024-08-06",
    input: [
        { role: "system", content: "You are a helpful math tutor. Guide the user through the solution step by step." },
        { role: "user", content: "how can I solve 8x + 7 = -23" }
    ],
    text: {
        format: {
            type: "json_schema",
            name: "math_response",
            schema: {
                type: "object",
                properties: {
                    steps: {
                        type: "array",
                        items: {
                            type: "object",
                            properties: {
                                explanation: { type: "string" },
                                output: { type: "string" }
                            },
                            required: ["explanation", "output"],
                            additionalProperties: false
                        }
                    },
                    final_answer: { type: "string" }
                },
                required: ["steps", "final_answer"],
                additionalProperties: false
            },
            strict: true
        }
    }
});

console.log(response.output_text);
```

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-2024-08-06",
    "input": [
      {
        "role": "system",
        "content": "You are a helpful math tutor. Guide the user through the solution step by step."
      },
      {
        "role": "user",
        "content": "how can I solve 8x + 7 = -23"
      }
    ],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "math_response",
        "schema": {
          "type": "object",
          "properties": {
            "steps": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "explanation": { "type": "string" },
                  "output": { "type": "string" }
                },
                "required": ["explanation", "output"],
                "additionalProperties": false
              }
            },
            "final_answer": { "type": "string" }
          },
          "required": ["steps", "final_answer"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  }'
```

**Note:** the first request you make with any schema will have additional latency as our API processes the schema, but subsequent requests with the same schema will not have additional latency.

Step 3: Handle edge cases

In some cases, the model might not generate a valid response that matches the provided JSON schema.

This can happen in the case of a refusal, if the model refuses to answer for safety reasons, or if for example you reach a max tokens limit and the response is incomplete.

```javascript
try {
  const response = await openai.responses.create({
    model: "gpt-4o-2024-08-06",
    input: [{
        role: "system",
        content: "You are a helpful math tutor. Guide the user through the solution step by step.",
      },
      {
        role: "user",
        content: "how can I solve 8x + 7 = -23"
      },
    ],
    max_output_tokens: 50,
    text: {
      format: {
        type: "json_schema",
        name: "math_response",
        schema: {
          type: "object",
          properties: {
            steps: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  explanation: {
                    type: "string"
                  },
                  output: {
                    type: "string"
                  },
                },
                required: ["explanation", "output"],
                additionalProperties: false,
              },
            },
            final_answer: {
              type: "string"
            },
          },
          required: ["steps", "final_answer"],
          additionalProperties: false,
        },
        strict: true,
      },
    }
  });

  if (response.status === "incomplete" && response.incomplete_details.reason === "max_output_tokens") {
    // Handle the case where the model did not return a complete response
    throw new Error("Incomplete response");
  }

  const math_response = response.output[0].content[0];

  if (math_response.type === "refusal") {
    // handle refusal
    console.log(math_response.refusal);
  } else if (math_response.type === "output_text") {
    console.log(math_response.text);
  } else {
    throw new Error("No response content");
  }
} catch (e) {
  // Handle edge cases
  console.error(e);
}
```

```python
try:
    response = client.responses.create(
        model="gpt-4o-2024-08-06",
        input=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
            },
            {"role": "user", "content": "how can I solve 8x + 7 = -23"},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "math_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "explanation": {"type": "string"},
                                    "output": {"type": "string"},
                                },
                                "required": ["explanation", "output"],
                                "additionalProperties": False,
                            },
                        },
                        "final_answer": {"type": "string"},
                    },
                    "required": ["steps", "final_answer"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    )
except Exception as e:
    # handle errors like finish_reason, refusal, content_filter, etc.
    pass
```

### 

Refusals with Structured Outputs

When using Structured Outputs with user-generated input, OpenAI models may occasionally refuse to fulfill the request for safety reasons. Since a refusal does not necessarily follow the schema you have supplied in `response_format`, the API response will include a new field called `refusal` to indicate that the model refused to fulfill the request.

When the `refusal` property appears in your output object, you might present the refusal in your UI, or include conditional logic in code that consumes the response to handle the case of a refused request.

```python
class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
steps: list[Step]
final_answer: str

completion = client.chat.completions.parse(
model="gpt-4o-2024-08-06",
messages=[
{"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
{"role": "user", "content": "how can I solve 8x + 7 = -23"}
],
response_format=MathReasoning,
)

math_reasoning = completion.choices[0].message

# If the model refuses to respond, you will get a refusal message

if (math_reasoning.refusal):
print(math_reasoning.refusal)
else:
print(math_reasoning.parsed)
```

```javascript
const Step = z.object({
explanation: z.string(),
output: z.string(),
});

const MathReasoning = z.object({
steps: z.array(Step),
final_answer: z.string(),
});

const completion = await openai.chat.completions.parse({
model: "gpt-4o-2024-08-06",
messages: [
{ role: "system", content: "You are a helpful math tutor. Guide the user through the solution step by step." },
{ role: "user", content: "how can I solve 8x + 7 = -23" },
],
response_format: zodResponseFormat(MathReasoning, "math_reasoning"),
});

const math_reasoning = completion.choices[0].message

// If the model refuses to respond, you will get a refusal message
if (math_reasoning.refusal) {
console.log(math_reasoning.refusal);
} else {
console.log(math_reasoning.parsed);
}
```

The API response from a refusal will look something like this:

```json
{
  "id": "resp_1234567890",
  "object": "response",
  "created_at": 1721596428,
  "status": "completed",
  "error": null,
  "incomplete_details": null,
  "input": [],
  "instructions": null,
  "max_output_tokens": null,
  "model": "gpt-4o-2024-08-06",
  "output": [{
    "id": "msg_1234567890",
    "type": "message",
    "role": "assistant",
    "content": [
      {
        "type": "refusal",
        "refusal": "I'm sorry, I cannot assist with that request."
      }
    ]
  }],
  "usage": {
    "input_tokens": 81,
    "output_tokens": 11,
    "total_tokens": 92,
    "output_tokens_details": {
      "reasoning_tokens": 0,
    }
  },
}
```

### 

Tips and best practices

#### Handling user-generated input

If your application is using user-generated input, make sure your prompt includes instructions on how to handle situations where the input cannot result in a valid response.

The model will always try to adhere to the provided schema, which can result in hallucinations if the input is completely unrelated to the schema.

You could include language in your prompt to specify that you want to return empty parameters, or a specific sentence, if the model detects that the input is incompatible with the task.

#### Handling mistakes

Structured Outputs can still contain mistakes. If you see mistakes, try adjusting your instructions, providing examples in the system instructions, or splitting tasks into simpler subtasks. Refer to the [prompt engineering guide](/docs/guides/prompt-engineering) for more guidance on how to tweak your inputs.

#### Avoid JSON schema divergence

To prevent your JSON Schema and corresponding types in your programming language from diverging, we strongly recommend using the native Pydantic/zod sdk support.

If you prefer to specify the JSON schema directly, you could add CI rules that flag when either the JSON schema or underlying data objects are edited, or add a CI step that auto-generates the JSON Schema from type definitions (or vice-versa).


## Pexels API Technical Documentation

The Pexels API is a **RESTful JSON API** that enables programmatic access to the entire Pexels library of photos and videos, all available free of charge.

### Integration Basics

#### Base URLs
For historical reasons, endpoints are split across two base URLs:

*   **Photos and Collections:** `https://api.pexels.com/v1/`
*   **Videos:** `https://api.pexels.com/videos/`

#### Authorization
Authorization is **required** for all Pexels API requests.

*   **Requirement:** An API key, which can be instantly requested by anyone with a Pexels account.
*   **Method:** Include the API key by adding an **`Authorization` header** to every request.
*   **Example:** `curl -H "Authorization: YOUR_API_KEY" \ "https://api.pexels.com/v1/search?query=people"`

#### Usage Guidelines and Rate Limits
*   **Attribution:** Always show a **prominent link back to Pexels** (e.g., using a text link like "Photos provided by Pexels" or the Pexels logo).
*   **Credit:** Always credit the photographers when possible (e.g., "Photo by John Doe on Pexels" with a link to the photo page on Pexels).
*   **Abuse Policy:** Do not copy or replicate core Pexels functionality (e.g., creating a wallpaper app). Abuse, including attempting to bypass the rate limit, will lead to termination of API access.
*   **Default Rate Limit:** The API is rate-limited to **200 requests per hour** and **20,000 requests per month**. Higher limits may be requested by contacting Pexels and providing examples/demos demonstrating proper attribution.

#### Rate Limit Response Headers
Successful HTTP responses (2xx) from the Pexels API include three headers that help manage your quota:

| Response Header | Meaning |
| :--- | :--- |
| `X-Ratelimit-Limit` | Your total request limit for the monthly period. |
| `X-Ratelimit-Remaining` | How many of these requests remain. |
| `X-Ratelimit-Reset` | UNIX timestamp of when the current monthly period will roll over. |

*(Note: These headers are not included in non-successful responses, such as `429 Too Many Requests` which indicates the rate limit has been exceeded).*

### General Pagination Parameters

Most endpoints return multiple records and are paginated, supporting a maximum of **80** results per request.

| Parameter | Type | Required | Description | Default | Maximum |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `page` | integer | optional | The page number being requested. | 1 | |
| `per_page` | integer | optional | The number of results requested per page. | 15 | 80 |

#### Common Pagination Response Attributes

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `page` | integer | The current page number. |
| `per_page` | integer | The number of results returned with each page. |
| `total_results` | integer | The total number of results for the request. |
| `next_page` | string | URL for the next page of results (only returned if applicable). |
| `prev_page` | string | URL for the previous page of results (only returned if applicable). |

***

