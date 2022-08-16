import asyncio
import csv
import datetime
from pyppeteer import launch

URLS = [
  "https://www.paylab.com/eg/salaryinfo/administration?lang=en",
  "https://www.paylab.com/eg/salaryinfo/agriculture-food-industry?lang=en",
  "https://www.paylab.com/eg/salaryinfo/arts-culture?lang=en",
  "https://www.paylab.com/eg/salaryinfo/banking?lang=en",
  "https://www.paylab.com/eg/salaryinfo/car-industry?lang=en",
  "https://www.paylab.com/eg/salaryinfo/chemical-industry?lang=en",
  "https://www.paylab.com/eg/salaryinfo/commerce?lang=en",
  "https://www.paylab.com/eg/salaryinfo/construction-real-estate?lang=en",
  "https://www.paylab.com/eg/salaryinfo/customer-support?lang=en",
  "https://www.paylab.com/eg/salaryinfo/economy-finance-accountancy?lang=en",
  "https://www.paylab.com/eg/salaryinfo/education-science-research?lang=en",
  "https://www.paylab.com/eg/salaryinfo/electrical-power-engineering?lang=en",
  "https://www.paylab.com/eg/salaryinfo/general-labour?lang=en",
  "https://www.paylab.com/eg/salaryinfo/human-resources?lang=en",
  "https://www.paylab.com/eg/salaryinfo/information-technology?lang=en",
  "https://www.paylab.com/eg/salaryinfo/insurance?lang=en",
  "https://www.paylab.com/eg/salaryinfo/journalism-printing-arts-media?lang=en",
  "https://www.paylab.com/eg/salaryinfo/journalism-printing-arts-media?lang=en",
  "https://www.paylab.com/eg/salaryinfo/law-legislation?lang=en",
  "https://www.paylab.com/eg/salaryinfo/leasing?lang=en",
  "https://www.paylab.com/eg/salaryinfo/management?lang=en",
  "https://www.paylab.com/eg/salaryinfo/marketing-advertising-pr?lang=en",
  "https://www.paylab.com/eg/salaryinfo/mechanical-engineering?lang=en",
  "https://www.paylab.com/eg/salaryinfo/medicine-social-care?lang=en",
  "https://www.paylab.com/eg/salaryinfo/mining-metallurgy?lang=en",
  "https://www.paylab.com/eg/salaryinfo/pharmaceutical-industry?lang=en",
  "https://www.paylab.com/eg/salaryinfo/production?lang=en",
  "https://www.paylab.com/eg/salaryinfo/public-administration-self-governance?lang=en",
  "https://www.paylab.com/eg/salaryinfo/quality-management?lang=en",
  "https://www.paylab.com/eg/salaryinfo/security-protection?lang=en",
  "https://www.paylab.com/eg/salaryinfo/service-industries?lang=en",
  "https://www.paylab.com/eg/salaryinfo/technology-development?lang=en",
  "https://www.paylab.com/eg/salaryinfo/telecommunications?lang=en",
  "https://www.paylab.com/eg/salaryinfo/textile-leather-apparel-industry?lang=en",
  "https://www.paylab.com/eg/salaryinfo/top-management?lang=en",
  "https://www.paylab.com/eg/salaryinfo/tourism-gastronomy-hotel-business?lang=en",
  "https://www.paylab.com/eg/salaryinfo/translating-interpreting?lang=en",
  "https://www.paylab.com/eg/salaryinfo/transport-haulage-logistics?lang=en",
  "https://www.paylab.com/eg/salaryinfo/water-management-forestry-environment?lang=en",
  "https://www.paylab.com/eg/salaryinfo/wood-processing-industry?lang=en",
]
csvFriendlyData = []

async def getSalary(URL):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(URL)    

    try:
        categorySalaries = await page.evaluate('''() => {
            allSalaries = []
            extracted = document.querySelectorAll(".category-full")
            for (i = 0; i < extracted.length; i++) {
                hyphenIndex = extracted[i].children[0].children[1].innerText.indexOf("-")
                startSalary = extracted[i].children[0].children[1].innerText.slice(0, hyphenIndex - 1 ).replace(",", "")
                endSalary = extracted[i].children[0].children[1].innerText.slice(hyphenIndex + 2).replace(" EGP", "").replace(",", "") 
                jobTitle = extracted[i].children[0].children[0].innerText
                average = (parseInt(startSalary) + parseInt(endSalary)) / 2
                allSalaries.push({ "Job Title": jobTitle, "Start Salary": startSalary, "End Salary": endSalary, "Average Salary": average })
            }
            return allSalaries
        }''')
        
        print(categorySalaries)
        csvFriendlyData.extend(categorySalaries)
        await browser.close()

    except Exception as e:
        print("error", e)
        await browser.close()


print("Script has started running 🏃...")
startTime = datetime.datetime.now()

for URL in URLS:
    asyncio.get_event_loop().run_until_complete(getSalary(URL))
    print("✅ Category Done")

with open('salaries.csv', 'w') as csvfile:
    fieldnames = ['Job Title', 'Start Salary', 'End Salary', 'Average Salary']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in csvFriendlyData:
        writer.writerow(data)

endTime = datetime.datetime.now()
print("Script took", endTime - startTime, "to run")
print("Script has stopped 🧎...")
