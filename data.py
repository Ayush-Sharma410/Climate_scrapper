import asyncio
from pyppeteer import launch
import csv
import re
years = [2015,2016,2017,2018,2019,2020,2021]
cities = ['ludhiana', 'agra', 'faridabad', 'meerut', 'varanasi', 'srinagar', 'amritsar', 'allahabad', 'jodhpur', 'chandigarh', 'kota', 'bareilly', 'moradabad', 'gurgaon', 'aligarh', 'jalandhar', 'saharanpur', 'gorakhpur', 'bikaner', 'noida', 'firozabad', 'dehradun', 'ajmer', 'loni', 'jhansi', 'jammu']
async def scrape_week_data(city,year,month,day):
    try:
        browser = await launch({"headless": True})
        page = await browser.newPage()
        url = f'https://www.wunderground.com/history/weekly/in/{city}/VIDD/date/{year}-{month}-{day}'
        await page.goto(url)

        # Sleep for 10 seconds
        await asyncio.sleep(10)
        try:
        # Wait for a specific element to be present on the page
            await page.waitForSelector('tbody .ng-star-inserted', {'timeout': 30000})
        
            # Get the result of elements with the class .ng-star-inserted inside td elements
            result = await page.evaluate('''() => {
                const elements = document.querySelectorAll('tbody .ng-star-inserted');
                return Array.from(elements).map(element => element.innerText);
            }''')
        except:
            result=None
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser in the finally block to ensure it gets closed even if an exception occurs
        await browser.close()

async def main():
    try:
        with open('output3.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='\t')
            
            # Write the header
            csv_writer.writerow(['Temperature (°F)', 'Max', 'Average', 'Min'])
            for city in cities:
                for year in years:
                    for month in range(1,13):  # Adjust the range for the desired years
                        day=1
                        while day<30:  # Adjust the range for the desired weeks
                            week_data = await scrape_week_data(city,year,month,day)
                            day=day+7
                            
                            try:
                            # Write the data to the CSV file
                                for line in week_data:
                                    if 'Sea Level Pressure' in line:
                                        break
                                    # Split the line into columns
                                    columns = line.strip().split('\t')
                                    
                                    # Write the columns to the CSV file, including the week information
                                    if any(not re.match(r'^\d+$', column) for column in columns):
                                        csv_writer.writerow([f'City-{city} Year-{year} Month-{month} Week-{day//7},'] + [column if i == 0 else f",{column}" for i, column in enumerate(columns)])
                            except:
                                  csv_writer.writerow([f'City-{city} Year-{year} Month-{month} Week-{day//7},'] + [])

        print("CSV file generated: output.csv")
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.get_event_loop().run_until_complete(main())
