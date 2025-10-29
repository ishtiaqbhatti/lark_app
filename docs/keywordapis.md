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

For example, for the `["domain_rank": "num"]` we can use these operators `<`, `<=`, `>`, `>=`, `=`, `<>`, `in`, `not_in`.

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
 