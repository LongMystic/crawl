import requests
import json
import pandas as pd
import time

payload = {}
headers = {
  'accept': 'application/json, text/plain, /',
  'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
  'priority': 'u=1, i',
  'referer': 'https://www.lazada.vn/',
  'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
  'x-csrf-token': 'f353351edb777',
  'Cookie': '_wpkreporterwid=a14418aa-b1b9-4a16-9dbd-cf57cc091bc5; __itrace_wid=0918f5cd-3f3f-4e85-1008-16aed9211626; t_fv=1755228617874; t_uid=AhAlssaMEY2QkxuluCUbhz79ANKqcOtP; hng=VN|en|VND|704; lwrid=AgGYq8c8xGrSClk7VTOjxe5uI61J; _m_h5_tk=d221084a392f8ee0aefe5b3c2bdf5e1a_1755237978016; _m_h5_tk_enc=8798cb8dd313024911271e150cdf3640; lzd_cid=4d7c42dc-0889-4a69-b74f-0960790d0625; lzd_sid=1bde2a2490b2f48d352306e388c464fe; tb_token=f353351edb777; cna=ypclIflJQA0CAXZGgSNJJHM6; xlly_s=1; lwrtk=AAIEaJ8aStRyXTVXCGwOyrmnSGGdvexpfR3HHQo84j3AF8Ti3O08jq8=; LZD_WEB_TRACER_ROOT_SPAN_ID=07b23640aabf9a64; LZD_WEB_TRACER_TRACE_ID=39f233d2bc2d4dcbb12a7327cc4128d2; isg=BKGhh-tvbe4dZcEa2uyWYmjgsGu7ThVAJ_y__gNyt6nGasg8SpvCEGXhzIZsoq14; tfstk=ftImwma-dQGIrBlDdzxblS1Wf1a-Mjt6w1n96hdazQRSMjnAQRxGn1jThOJOS_XCssd45-AWaBIM3FIO3d8Np_CvuCItb_xf2Zn9MStGQ6Kg9WELvt6kchPL9Dm-YLtXIqJ2ufKradawJmQTvt6jUbfp--qKINeMRjAN_ERyzKOy3dRw38Yypd-Z0FoqzbRWQFU_gjA5k0vpu8usMuoaTlU2ttRox6sy3ROzABoamgJcEvXDZdvGqKvDtFy1iWShLtSBIGwESCx1usp5skVk4ifc0Uxgj0tAKa5DrZViqU_PdG8lPW0Cdt5c8eS4q85Ga9_B0iPsDI_NUGRR0RnMTwBBqgrtz2zCGc9zBgus5EJWEBF3ljxoTmPo382oRrT2FKFLE80_SXiZxWeuE2MwuL9Y9; epssw=10*TS6ss6zOMBAdkOxa6su0wT394IukxjF9oWmnAas3bg3sssKsB4N3s3EEU7IQtNFpFUJ6UsssUNxebND6MHM8J6BDsFV6DxbGhvccTr1fKuUGiROQzFPKakOWvTUssHJIwkit7YVGtRZusFxaBPLssRftg3sakD_UWfKB9MAqF5EaF6uGIjTl2DAMDPBdiK15Cr1MIPNmiMdrJUsB-Qrg46IOfedzoPOOFCpDmWCLMwlWKhuw4jsddN_Sd35ndiuaORrQgNvvbBKDqNMobR3ss7RQC1uSUO5siNVZHWDLlC2QQIs3UAvttL6x9TeTkw7pT2zksK6BNezFi4brmcn4KiQJa3I_FPNe6DaHhPfB; t_sid=zkVZPhr5pzsf77eO3xP5c9ozdIO74r8X; utm_channel=NA'
}

data = {
    "product_id": [],
    "product_name": [],
    "barcode": [],
    "brand": [],
    "image": [],
    "description": [],
    "url": []
}

p_id = 0
for i in range(200):
    url = f"https://www.lazada.vn/tag/bánh-trung-thu/?ajax=true&catalog_redirect_tag=true&isFirstRequest=true&page={i}&q=bánh trung thu&spm=a2o4n.tm80243110.search.d_go"
    
    try:
        time.sleep(2)
        response = requests.request("GET", url, headers=headers, data=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            try:
                # Parse JSON from response content
                json_response = response.json()
                
                # Check if the expected structure exists
                if "mods" in json_response and "listItems" in json_response["mods"]:
                    item_list = json_response["mods"]["listItems"]
                    
                    for item in item_list:
                        data["product_id"].append(p_id)
                        data["product_name"].append(item.get("name"))
                        data["barcode"].append(item.get("sku"))
                        data["brand"].append(item.get("brandName"))
                        data["image"].append(item.get("image"))
                        data["description"].append(None)
                        data["url"].append(item.get("itemUrl"))
                        p_id += 1
                    
                    print(f"Crawl page {i} successfully - Found {len(item_list)} items")
                else:
                    print(f"Page {i}: Unexpected response structure")
                    print(f"Response keys: {list(json_response.keys())}")
                    
            except json.JSONDecodeError as json_err:
                print(f"Page {i}: Failed to parse JSON - {json_err}")
                print(f"Response content preview: {response.text[:200]}...")
        else:
            print(f"Page {i}: HTTP {response.status_code} - {response.reason}")
            
    except Exception as e:
        print(f"Crawling stopped at page {i} due to error:")
        print(e)
        break

# Save data to CSV
if data["product_id"]:
    df = pd.DataFrame(data)
    df.to_csv("product_detail.csv", index=False)
    print(f"\nCrawling completed! Total products collected: {len(data['product_id'])}")
    print(f"Data saved to product_detail.csv")
else:
    print("No data was collected. Please check the crawling logic.")