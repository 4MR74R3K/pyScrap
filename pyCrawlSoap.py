import asyncio
import csv
import datetime
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

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

print("Script has started running 🏃...")
startTime = datetime.datetime.now()

async def main(URL, pbar):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    allPositions = []
    results = soup.select(".category-full")

    try:
        for result in results:
            page = requests.get(result.get('href'))
            soup = BeautifulSoup(page.content, "html.parser")
            ranking = ""
            if soup.select(".card-footer"):
                matchingString = ". place"
                if(matchingString in soup.select(".card-footer")[0].get_text().strip()):
                    indexOfAPlace = soup.select(".card-footer")[0].get_text().strip().find(matchingString)
                    ranking = soup.select(".card-footer")[0].getText().strip()[:indexOfAPlace]
                else:
                    ranking = "N/A"
            if soup.select('h1'):
                title = soup.select('h1')[0]
            i = 0
            position = ""
            category = ""
            for sen in title.strings:
                if i == 0:
                    position = sen.strip()
                    i += 1
                else:
                    category += sen.strip()

            if soup.select(".range-chart-row-value"):
                startSalary = soup.select(".range-chart-row-value > span")[1].getText().replace(",", "").replace("K", "000")[:-3].strip()
                endSalary = soup.select(".range-chart-row-value > span")[3].getText().replace(",", "").replace("K", "000")[:-3].strip()
                averageSalary = (float(startSalary) + float(endSalary)) / 2
            else:
                averageSalary = "N/A"
                startSalary = "N/A"
                endSalary = "N/A"

            # print({
            #     "position": position,
            #     "category": category,
            #     "startSalary": startSalary,
            #     "endSalary": endSalary,
            #     "averageSalary": averageSalary,
            #     "ranking": ranking,
            # })
 
            csvFriendlyData.append({"Job Title": position, "Category": category, "Start Salary": startSalary, "End Salary": endSalary, "Average Salary": averageSalary, "Ranking": ranking})
        pbar.update(1)

    except Exception as e:
        print("⚠️ error", e)
        pass

pbar = tqdm(total=len(URLS), colour="green")

for URL in URLS:
    asyncio.get_event_loop().run_until_complete(main(URL, pbar))
    
with open('salaries.csv', 'w') as csvfile:
    fieldnames = ['Job Title', 'Category', 'Start Salary', 'End Salary', 'Average Salary', 'Ranking']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in csvFriendlyData:
        writer.writerow(data)
        
pbar.close()

endTime = datetime.datetime.now()
print("Script took", endTime - startTime, "to run")
print("Script has stopped 🧎...")
