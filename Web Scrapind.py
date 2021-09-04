import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest


result = requests.get("https://wuzzuf.net/search/jobs/?a=hpb&q=python&start=0")
src = result.content



soup = BeautifulSoup(src, "lxml")




job_title = []
company_name = []
location_name = []
job_skill = []
links = []
salaries = []
posts = []
Job_Requirements = []




num_of_page = 0

while True:
    
    try:
    
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={num_of_page}")
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        job_titles = soup.find_all("h2", {"class" : "css-m604qf"})
        company_names = soup.find_all("a", {"class" : "css-17s97q8"})
        location_names = soup.find_all("span", {"class" : "css-5wys0k"})
        job_skills = soup.find_all("div", {"class" : "css-y4udm8"})
        new_job_posted = soup.find_all("div", {"class" : "css-4c4ojb"})
        old_job_posted = soup.find_all("div", {"class" : "css-do6t5g"})
        posted =[*new_job_posted, *old_job_posted]

        for i in range( len(job_titles)):
            job_title.append(job_titles[i].get_text(strip=True))
            links.append(job_titles[i].find("a").attrs["href"])
            company_name.append(company_names[i].get_text(strip=True))
            location_name.append(location_names[i].get_text(strip=True))
            job_skill.append(job_skills[i].get_text(strip=True))
            posts.append(posted[i].get_text(strip=True))
        #job_skill[0] = "Computer Science·Django·Engineering·Flask·HTML5·Information Technology (IT)·JavaScript·Python·ORM·Software Development"

        soup = BeautifulSoup(src, "lxml")
        Jobs_number = int( soup.find("strong").get_text(strip=True) )

        print(f"the Current Page Number is : {num_of_page}")

        num_of_page = num_of_page + 1

        if (num_of_page > Jobs_number // 15):
            Jobs_Showing  = soup.find("li", {"class":"css-8neukt"}).get_text(strip=True)
            print("Padges ended \n")
            print(Jobs_Showing + "\n")
            break
            
    except Exception as error:
        print(error)
        break
        
n = 1        
for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    Job_Requirement = soup.find("div", {"class" : "css-1t5f0fr"})
    Job_Requirements.append(Job_Requirement.get_text(strip=True))
    print(f"Number of Job is : {n}")
    n = n + 1
    #job_salarys = soup.find("span", {"class" : "css-4xky9y"})
    #salaries.append(job_salarys.get_text(strip=True))




file_list = [job_title, company_name, posts, location_name, job_skill, Job_Requirements, links]
exported = zip_longest(*file_list)

with open("E:\\other\\Epsilon_Ai\\info\\my_progect\\All Job.csv", "w", newline = "", encoding='utf8') as my_file:
    wr = csv.writer(my_file)
    wr.writerow(["job_title", "company_name", "posts", "location_name", "job_skill", "Job_Requirements", "links"])
    wr.writerows(exported)
