# This made to send a bucket of numbers the WA API to check if the number is valid
#
1. The script takes the numbers from each tab on the spreadsheet.
2. For every 500 numbers the script will send a request to WA API and get a JSON object .
3. After we have a JSON object with invalid/valid numbers the script will write it to the g-spreadsheet.
2. For every 500 numbers, the script will send a request to WA API and gets a JSON object back from Whatsapp.