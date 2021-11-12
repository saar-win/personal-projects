# Send a bucket of numbers to the WA API to check if the number is valid
#
1. The script takes the numbers from each tab in the spreadsheet.
2. For every 500 numbers the script send a request to WA API and get a JSON object.
3. Get a JSON object with invalid/valid numbers, write it to the g-spreadsheet.
