import asyncio
from pyppeteer import launch
import csv
import re
years = [2017,2018,2019,2020,2021]
cities = ['new-delhi/VIDD']
async def scrape_humidity_data(city,year,month,day):
    try:
        browser = await launch({"headless": True})
        page = await browser.newPage()
        url = f'https://www.wunderground.com/history/weekly/in/{city}/date/{year}-{month}-{day}'
        await page.goto(url)

        # Sleep for 10 seconds
        await asyncio.sleep(10)
        try:
        # Wait for a specific element to be present on the page
            await page.waitForSelector('td .ng-star-inserted', {'timeout': 60000})
        
            # Get the result of elements with the class .ng-star-inserted inside td elements
            result = await page.evaluate('''() => {
                const elements = document.querySelectorAll('td .ng-star-inserted');
                return Array.from(elements).map(element => element.innerText);
            }''')
            
            result_humidty = result
            
            # print(type(result))
        except:
            result_humidty=None
            
            
        return result_humidty
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f'{city}/date/{year}-{month}-{day}')
    finally:
        # Close the browser in the finally block to ensure it gets closed even if an exception occurs
        await browser.close()

async def main():
    try:
        with open('output.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='\t')
            
            # Write the header
            csv_writer.writerow(['Temperature (°F)','Humidity(%)','Pressure(in)'])
            for city in cities:
                for year in years:
                    for month in range(1,13):  # Adjust the range for the desired years
                        day=1
                        while day<30: 
                                try:
                                    # Adjust the range for the desired weeks
                                    data = await scrape_humidity_data(city,year,month,day)
                                    
                                    humidity_data = data[80:109]
                                    
                                    pressure_data = data[144:173]

                                    
                                    # Write the data to the CSV file
                                    for humidity_line,pressure_line in zip(humidity_data,pressure_data):
                                        
                                        try:    
                                            
                                            # Split the line into columns
                                            
                                            humidity_columns = humidity_line.strip().split('\t')
                                            pressure_columns = pressure_line.strip().split('\t')
                                            
                                            if len(humidity_columns)>1:                                    
                                            # Write the columns to the CSV file, including the week information
                                                if any(not re.match(r'^\d+$', column) for column in humidity_columns):
                                                    csv_writer.writerow([f'City-{city} Year-{year} Month-{month} Week-{(day//7) + 1},']+ [f"{column}," for i, column in enumerate(humidity_columns)] + [f",{column}" for i, column in enumerate(pressure_columns)]  )
                                        except:
                                            csv_writer.writerow([f'City-{city} Year-{year} Month-{month} Week-{(day//7) + 1},'] + [])
                                except:
                                        csv_writer.writerow([f'City-{city} Year-{year} Month-{month} Week-{(day//7) + 1},'] + [])      
                                day=day+7

        print("CSV file generated: output.csv")
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.get_event_loop().run_until_complete(main())
