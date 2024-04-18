import requests
from bs4 import BeautifulSoup
import csv
import re
import webbrowser
import base64
#from PIL import Image
from io import BytesIO
import retrying

@retrying.retry(stop_max_attempt_number=3)
def scrape_contact_data(url, page_number):
    # Send a GET request to the URL
    #open(url)
    response = requests.get(url,timeout=30)
    src=response.content
    #print(src)
    global counter
    global Contact_details
    global person_No
    Contact_details=[]
    #chrome_browser = webbrowser.open(url)

    # Open the URL in Chrome
    #chrome_browser.open(url)

    #print(src)

    # Check if the request was successful
    if response.status_code == 200:
       
        soup = BeautifulSoup(src, "lxml")
       # Contact_details=[]
        # Find all elements containing person data
        person_elements = soup.find_all("div", {'class': "panelMember"})
        total_contacts=len(person_elements)

        


        def get_contact_data(person_elements):
            global person_No
            person_No=person_No+1
            name = person_elements.contents[1].find('h4').text.strip()
            jobTitle = person_elements.contents[1].find('p', class_='jobTitle').text.strip()
            country = person_elements.contents[1].find('p', class_='location' ).text.strip() 
            Branches = person_elements.contents[1].find ('p', class_='branches' ).text 
            Branches=Branches.replace('Branches:','')
            Branches=Branches.replace('','')

            Branches=Branches.lstrip()

            profile= person_elements.contents[3].find('a', class_='view')
            pattern = r'href="([^"]+)"'
            match = re.search(pattern, str(profile))
            profile_url=match.group(1)
            
            response = requests.get(base_url+profile_url)
            src2=response.content
            soup2 = BeautifulSoup(src2, "lxml")

            profile_image_text = soup2.find("div", {'class': "profileImage"})
            #print(profile_image_text)
            # Define a regular expression pattern to extract the URL from the style attribute
            pattern = r"url\('([^']+)'"

            # Use the findall() function from the re module to find all matches of the pattern in the HTML content
            matches = re.findall(pattern, str(profile_image_text))

            # If matches are found, extract the URL from the first match
            ##########################Photo
            #if matches:
             #   profile_image_url = matches[0]
            #photo=base_url+profile_image_url
            if matches:
              profile_image_url = matches[0]
            else:
              profile_image_url = None

            photo = base_url + profile_image_url if profile_image_url else ""
            if 'avatar' in photo:
                photo = " "
       #     image_data = download_image(photo)
        #    if  photo :
               # Resize the image
       #        resized_image_data = resize_image(image_data)
            # Encode the resized image as base64
        #       base64_image = base64.b64encode(resized_image_data).decode('utf-8')
        #    else:
        #        base64_image=""


            #print(image_url)
            ##image_data = download_image(image_url)
            #imshow(image_data)
            ##if image_data:
                # Convert image data to base64 encoding
            ##    base64_image = base64.b64encode(image_data).decode('utf-8')
            Grade_String = soup2.find("div", {'class': "memberProfileIntro"})
            p_tags = Grade_String.find_all('p')
            Grade=""
            for p_tag in p_tags:
               if 'FCIArb' in p_tag.text:
                  Grade="F"
                 # print(Grade)

               elif 'MCIArb' in p_tag.text:
                   Grade="M"
                  # print(Grade)

               elif 'ACIArb' in p_tag.text:
                   Grade="A"
                  # print(Grade)

           # print (Grade_String)
            profile_elements2 = soup2.find("div", {'class': "memberContactDetails"})
            #print(profile_elements2)
           # email_tag = profile_elements2.find('a', href=True)
           # email_address = email_tag.get_text(strip=True)
            email_tag = profile_elements2.find('a', href=True)
            email_address = email_tag.get_text(strip=True) if email_tag else ""

            
            # Find the telephone number
            telephone_number_element = profile_elements2.find('p', class_='memTelephone')
            if telephone_number_element:
                Mobile = telephone_number_element.find('a').text.strip()
            else:
                Mobile=" "

            # Find the company phone number
            company_phone_element = profile_elements2.find('h2', text='Company Details').find_next('p').find('a')
            if company_phone_element:
               company_number = company_phone_element.text.strip()
            else:
               company_number=""
    
            # Find the LinkedIn page
            linkedin_element = profile_elements2.find('p', class_='memLinkedIn')
            if linkedin_element:
              linkedin = linkedin_element.find('a')['href']
            else:
               linkedin = " "
            
            # Find the company name
            company_name_element = profile_elements2.find('h2', text='Company Details').find_next('p')
            company_name_text = ''
            if company_name_element:
               for element in company_name_element.contents:
                   if element.name == 'br':
                      break
                   company_name_text += str(element)

            company_name = company_name_text.strip()

           # other variable
            twitter_tag = profile_elements2.find('p', class_='memTwitter')
            if twitter_tag:
                twitter_link = twitter_tag.find('a')['href']
            else:
                twitter_link=""

            Contact_details.append({"Name":name,"Grade":Grade})
           # Contact_details.append({"No":person_No,"Serial Number":"","Name":name,"Grade":Grade,"Country":country,"Company":company_name,"Position":jobTitle,"E-mail":email_address,"Mobile Number":Mobile,"Company Number":company_number,"Linkedin":linkedin,"Photo":photo,"Address":"","Other":twitter_link})

        for i in range(total_contacts):
           get_contact_data(person_elements[i])
        keys=Contact_details[0].keys()
        with open("D:/org/BrainStorming/projects/WebScrap/scrap_All_data.csv",'a', encoding='utf-8') as output_file:
            dictwriter=csv.DictWriter(output_file,keys)
            if(counter==1):
              dictwriter.writeheader()
              counter=counter+1
            dictwriter.writerows(Contact_details)

            #for row in dictwriter:
            #  if row.strip():
            #     output_file.write(row)
                 #dictwriter.writerows(Contact_details)

        
def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None

def resize_image(image_data, size=(50, 50)):
    try:
        img = Image.open(BytesIO(image_data))
        img.thumbnail(size)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return buffered.getvalue()
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None



def main():
 global counter
 global base_url
 global Contact_details
 Contact_details=[]
 counter=1
 global person_No
 person_No=0
# URL of the website to scrape
#page_number=input("please enter page number:")
 pages=703
 base_url = 'https://www.ciarb.org/'
 for page_number in range (1,pages+1):
    #page_number=page_number
    url = 'https://www.ciarb.org/membership/member-directory?page='+str(page_number)
    scrape_contact_data(url,page_number)
    print("page_number:"+ str( page_number)+ "   ended")

main()    

