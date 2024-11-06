import asyncio
from pyppeteer import launch
import csv
import re
years = [2015,2016,2017,2018,2019,2020,2021]
cities = ['new-delhi/VIDD','jaipur/VIJP','lucknow/VILK','kanpur/VECX','ludhiana/VILD', 'agra/VIAG', 'srinagar/VISR', 'amritsar/VIAR', 'jodhpur/VIJO', 'chandigarh/VICG', 'kota/VIKO', 'moradabad/VIPT', 'gurgaon/VIDP','gorakhpur/VEGK', 'bikaner/VIBK','dehradun/VIDN', 'jhansi/VIJN', 'marh/VIJU']
async def scrape_humidity_data(city,year,month,day):
    try:
        browser = await launch({"headless": False})
        page = await browser.newPage()
        url = f'https://www.wunderground.com/history/weekly/in/{city}/date/{year}-{month}-{day}'
        await page.goto(url)

        # Sleep for 10 seconds
        await asyncio.sleep(10)
        try:
        # Wait for a specific element to be present on the page
            await page.waitForSelector('td .ng-star-inserted', {'timeout': 30000})
        
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
            csv_writer.writerow(['Temperature (°F)','Date','Humidity(%)','Pressure(in)'])
            for city in cities:
                for year in years:
                    for month in range(1,13):  # Adjust the range for the desired years
                        day=1
                        while day<30: 
                            try:      # Adjust the range for the desired weeks
                                data = await scrape_humidity_data(city,year,month,day)
                                
                                day=day+7
                                date = data[0:16]
                                humidity_data = data[80:109]
                                # print(humidity_data)
                                pressure_data = data[144:173]
                                # print(pressure_data)
                                
                                humidity_data = [column for column in humidity_columns if len(humidity_columns)>1]
                                pressure_data = [column for column in pressure_columns if len(pressure_columns)>1]
                                date = [column for column in date_columns if not '\n' in column ]
                                print(list(zip(date,humidity_data,pressure_data)))
                                
                                # Write the data to the CSV file
                                for date_line,humidity_line,pressure_line in zip(date,humidity_data,pressure_data):
                                    
                                    try:    
                                        
                                        # Split the line into columns
                                        date_columns = date_line.strip().split('\t')
                                        pressure_columns = pressure_line.strip().split('\t')
                                        humidity_columns = humidity_line.strip().split('\t')


                                                                         
                                        # Write the columns to the CSV file, including the week information
                                        if any(not re.match(r'^\d+$', column) for column in humidity_columns):
                                            csv_writer.writerow([f'City-{city} Year-{year} Month-{month} Week-{day//7},']+ [column if i == 0 else f"{column}," for i, column in enumerate(date_columns)]+[column if i == 0 else f"{column}," for i, column in enumerate(humidity_columns)] + [column if i == 0 else f",{column}" for i, column in enumerate(pressure_columns)] )
                                    except:
                                        csv_writer.writerow([f'City-{city} Year-{year} Month-{month} Week-{day//7},'] + [])
                            except:
                                 csv_writer.writerow([f'City-{city} Year-{year} Month-{month} Week-{day//7},'] + [])         
                                

        print("CSV file generated: output.csv")
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.get_event_loop().run_until_complete(main())
