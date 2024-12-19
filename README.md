# dap_accessibility_report
Exploring Accessibility Reporting with DAP and Pa11y:

At Instructure, we have a company tradition called _Dim the Lights_, which allows us to recharge or work on side projects. Last year, I used this time to brainstorm an out-of-the-box use case for our **Data Access Platform (DAP)**.

Initially, I considered experimenting with linear regression models, but my attention shifted to some of the common comments I’d heard about accessibility reporting in Canvas. My first instinct was to scrape data from my Canvas instance, but that approach didn’t feel right. Fortunately, DAP includes the **wiki pages table**, which already contains the HTML values of pages—no scraping required!

  **Step 1: Identifying Accessibility Issues**

With the data in hand, the next step was to identify accessibility issues within the pages. I started by looking into the accessibility tool built into Canvas, but I felt there was room for more depth. Enter trusty Google! After dodging bland AI-generated responses (please bring back the old Google 😅), I stumbled upon [Pa11y](https://github.com/pa11y/pa11y).

**Pa11y** is a CLI tool that automates accessibility testing for HTML pages. By default, it adheres to WCAG 2.1 Level AAA standards—exactly the level of rigor I wanted. Time to get to work.

  **Step 2: Preparing the Data**

To keep things simple for this proof of concept, I selected a Canvas instance with limited data. I synchronized the DAP tables to my Postgres instance and wrote a quick SQL query to produce a CSV file containing the following columns: page ID, page title, course ID, teacher name, and body content. Once I had the CSV file, I was ready to dig into **Pa11y**.

  **Step 3: Running Accessibility Tests**

At first, I tried passing HTML values directly to Pa11y, but I quickly realized that it requires actual HTML files. After a bit of trial and error, I put together this Python script to process the CSV, generate HTML files, and run Pa11y tests. With this script, I was able to generate a report of all the accessibility issues! 🎉

**Step 4: Visualizing the Results**

While a CSV full of accessibility issues is functional, it’s not exactly user-friendly. To make the results more digestible, I turned to **Looker Studio** to create a [dashboard](https://lookerstudio.google.com/reporting/70da3b25-51b8-461b-876b-a2405bde8a33).

  

  

It’s not the prettiest dashboard I’ve ever built, but it works as a proof of concept!

  

**Reflection and Next Steps**

Looking back, here’s how this process could be improved for scalability:

• **Switch to JavaScript:** Implementing this in JavaScript would eliminate the need for Python’s subprocess calls.

• **Direct Integration:** Save the report to a Postgres table for direct integration with a dashboard builder.

• **Smarter Updates:** Use the _revision_ column in the wiki pages table to check if a page has been updated since the last report, reducing unnecessary HTML generation.

• **Instructor Notifications:** Leverage Pa11y’s recommendations to notify instructors of accessibility issues directly.
