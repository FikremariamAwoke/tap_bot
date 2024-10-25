const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');


const links = [
  // abi 1
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAHL1r0WAAAAAMvWvRaqmrp6%26user%3D%257B%2522id%2522%253A381540043%252C%2522first_name%2522%253A%2522Fikremariam%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522FikremariamA%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729800469%26hash%3D8b18c4845766c2d4bd6cfaafe25402710a55f39f6a592c9d16437fdf073d001e&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23232e39%22%2C%22section_bg_color%22%3A%22%231f2831%22%2C%22secondary_bg_color%22%3A%22%23161f25%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237f8c97%22%2C%22link_color%22%3A%22%236ab0d7%22%2C%22button_color%22%3A%22%2360b0e1%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23262e37%22%2C%22accent_text_color%22%3A%22%2371bbe4%22%2C%22section_header_text_color%22%3A%22%2384c9f1%22%2C%22subtitle_text_color%22%3A%22%237d888e%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230e1317%22%2C%22bottom_bar_bg_color%22%3A%22%23161f25%22%7D',
  // abi 2
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAFrllYPAwAAAGuWVg9dt0_v%26user%3D%257B%2522id%2522%253A6699783787%252C%2522first_name%2522%253A%2522Misc%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Misc77h%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729800510%26hash%3D77602adb10e129d34c6f2df1bd63afba347942427bad01bdbdcb18e6e54767c9&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230d1218%22%2C%22bottom_bar_bg_color%22%3A%22%23151e27%22%7D',
  // abi 3
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAENGAkYAwAAAA0YCRiecvPm%26user%3D%257B%2522id%2522%253A6845700109%252C%2522first_name%2522%253A%2522.._..%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522S63wa%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729800549%26hash%3Da52c79109862c576e4fdec5417607db5bdde255c9390038beeffd968e04c789a&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230d1218%22%2C%22bottom_bar_bg_color%22%3A%22%23151e27%22%7D',
  // abi 4
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAHvbigtAAAAAO9uKC1pt2ze%26user%3D%257B%2522id%2522%253A757624559%252C%2522first_name%2522%253A%2522S%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Zolatani%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729800609%26hash%3Da8dd3670f2c46a254fbc927ad9133950279aa8a9e2ea20d03c971722c9a8eb38&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230d1218%22%2C%22bottom_bar_bg_color%22%3A%22%23151e27%22%7D', 
  
  // ela 1
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAH4YfBhAgAAAPhh8GEv1b6B%26user%3D%257B%2522id%2522%253A5938110968%252C%2522first_name%2522%253A%2522Eliyas%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Eliyasassefa%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729707756%26hash%3Dea6597394da90660075334d113970569e8bd1576405d37d5cae0d7f4e9239b8f&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D', 
  // ela 2 hiwote account
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAHZPQAeAwAAANk9AB7uK6Ok%26user%3D%257B%2522id%2522%253A6945783257%252C%2522first_name%2522%253A%2522Hewot%2522%252C%2522last_name%2522%253A%2522H%2522%252C%2522username%2522%253A%2522Hewot1235%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729707915%26hash%3D4a832be891432a6a7a52c88d3676ed6329e2638de7a3c47f819e43b3b61b7940&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D',
  
  // bement
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAH0Pdx-AAAAAPQ93H5UoWXG%26user%3D%257B%2522id%2522%253A2128362996%252C%2522first_name%2522%253A%2522Bement%2522%252C%2522last_name%2522%253A%2522Awoke%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729791555%26hash%3Df704e9a9b89fe6d6360ab09b6731aff6fafe0be874aba5f3602916be17cb2ddb&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230d1218%22%2C%22bottom_bar_bg_color%22%3A%22%23151e27%22%7D',
  
  // simon 1 yared
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAGdwjo3AwAAAJ3COje5v7Fc%26user%3D%257B%2522id%2522%253A7369048733%252C%2522first_name%2522%253A%2522Yared%25C2%25A0%25F0%259F%2590%2588%25E2%2580%258D%25E2%25AC%259B%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729783328%26hash%3D2bbca6a8c275ab0de54a376398e7d3a5c8581f9044876a1d1b8cb84f02ab5e6a&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230d1218%22%2C%22bottom_bar_bg_color%22%3A%22%23151e27%22%7D',
  // simon 2 abel
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAH_USwBAwAAAP9RLAEsB7om%26user%3D%257B%2522id%2522%253A6462132735%252C%2522first_name%2522%253A%2522Abel%25C2%25A0%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Abelas24%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729783281%26hash%3Dd71543a1aaeeff9a708d43c3ec023d986bf55ae98ce4f6a3000d0f0240b21fa9&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230d1218%22%2C%22bottom_bar_bg_color%22%3A%22%23151e27%22%7D',
  // simon 3
  'https://tap1.urko.io/#tgWebAppData=query_id%3DAAENYTYXAAAAAA1hNhfo9K7g%26user%3D%257B%2522id%2522%253A389439757%252C%2522first_name%2522%253A%2522Simon%25F0%259F%258D%2585%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Simond27%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729783189%26hash%3D022c60e7e9da63b6433445fb2bbcbf6b13e4760a46f6aaf73e53f0ea6a1102c7&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230d1218%22%2C%22bottom_bar_bg_color%22%3A%22%23151e27%22%7D'
];

(async () => {
  // Define the local path of your custom script
  const customScriptPath = path.resolve(__dirname, 'custom_main.b930ae92.js');
  const customScriptContent = fs.readFileSync(customScriptPath, 'utf8');

  for (const link of links) {
    // Launch a new browser instance for each link
    const browser = await puppeteer.launch({ headless: true }); // Set to false to show UI
    const page = await browser.newPage();

    // Intercept requests
    await page.setRequestInterception(true);

    page.on('request', request => {
      if (request.url() === 'https://tap1.urko.io/static/js/main.b930ae92.js') {
        // Serve the custom script instead of fetching the original one
        request.respond({
          status: 200,
          contentType: 'application/javascript',
          body: customScriptContent,
        });
      } else {
        request.continue(); // For all other requests, continue as usual
      }
    });

    console.log(`opening the page: ${link}...\n`);
    try {
        // Navigate to the target page
        await page.goto(link, { waitUntil: 'networkidle2' });
    }  catch (error) {
        console.error("Error loading page:", error);
    }
    // Reload the page every 30 minutes (30 * 60 * 1000 milliseconds)
    setInterval(async () => {
      console.log(`Reloading the page: ${link}...`);
      try {
        await page.reload({ waitUntil: 'networkidle2' });
        console.log("Page reloaded successfully.\n");
    } catch (error) {
        console.error("Error reloading page:", error);
    }
    }, 10 * 60 * 1000); // 30 minutes in milliseconds
  }
})();