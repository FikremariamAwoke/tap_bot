const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');


// Function to read links from links.json
const readLinksFromJson = (filePath) => {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    const jsonData = JSON.parse(data);
    return jsonData.links.map(linkObject => linkObject.url); // Extract URLs
  } catch (error) {
    console.error("Error reading links.json:", error);
    return [];
  }
}

(async () => {
  // Define the local path of your custom script
  const customScriptPath = path.resolve(__dirname, 'custom_main.b930ae92.js');
  const customScriptContent = fs.readFileSync(customScriptPath, 'utf8');

  // Read links from links.json
  const links = readLinksFromJson(path.resolve(__dirname, 'links.json'));

  var count = 0

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

    count = count + 1;
    console.log(`opening the page ${count}: ${link}...\n`);
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