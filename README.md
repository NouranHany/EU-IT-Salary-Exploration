# EU-IT-Salary-Exploration 🌍💻💰
The aim of our project is to explore IT salaries in Europe and provide valuable insights and analysis to two key target audiences: employers who are establishing or already have an IT company, and individuals searching for jobs in the IT sector. Understanding and analyzing IT salaries in Europe is crucial for both employers and job seekers. Employers gain valuable insights into salary benchmarks, enabling them to attract and retain top talent through competitive compensation packages. Job seekers, on the other hand, benefit from access to crucial salary data, empowering them to negotiate fair salaries and make well-informed career decisions.

## Additional Resources 📚🔍
- **Story-telling Presentation**: For a visually engaging overview of our project and its findings, please check out our [presentation](https://www.canva.com/design/DAFjO_ghpQQ/tneO6Q2C7y2knc_7ECw9VQ/view?utm_content=DAFjO_ghpQQ&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink#1).

- **Project Document**: For detailed information on the cleaning and analysis processes, refer to our comprehensive [project document](./Report.pdf).

## Dataset 📊📂
Our project utilized an annual anonymous salary survey conducted among European IT specialists, with a focus on Germany. We combined three consecutive years of data (2018-2020) into a single dataset. The dataset exhibited inconsistencies both across survey years and within its own structure. However, we addressed and resolved these inconsistencies, successfully consolidating the data into a dataset comprising approximately 3000 records.

The raw dataset was sourced from Kaggle and can be found [here](https://www.kaggle.com/datasets/parulpandey/2020-it-salary-survey-for-eu-region)

## Data Preprocessing 🛠️
During the data preprocessing phase, we implemented several approaches to address the inconsistencies caused by survey respondents:

- **Normalization**: We performed data normalization by remove leading and trailing spaces, standardize letter cases, and handle aggregated values.
- **Grouping and Clustering**: We used ChatGPT and manual refinement to consolidate similar categories and reduce the number of unique values.
- **Filtering**: We applied filtering methods to remove low-frequency categories, eliminating unreliable or inconsistent data.
- **Spell Checking and Correction**: We employed manual checking and utilized the fuzzywuzzy library, leveraging Levenshtein Distance to correct spelling errors.
- **Outliers Removal**: We identified and removed outliers in the salary data to improve the overall statistical analysis.
- **Standardization**: We standardized certain attributes to ensure consistency in ranges and values. For example, "11-50" and "10-50" were unified as "10-50".
- **Extraction**: We extracted relevant information from text-based columns to obtain numeric values for further analysis.

## Questions ❓🔍
For each question, this project applies the data science 5 stage cycle and the epicycle. Here are the questions we have answered:

**How is the salary affected? 💰**

Q9:  What is the most paying position in Berlin? [answer](./Questions/D_Position_Salary_City.ipynb)  </br>
Q10: Can we infer that the most paying position in Berlin is the highest paid in all other cities? [answer](./Questions/I_City_Position_Salary.ipynb)  </br>
Q3: How does the salary for the same position differ from city to another? [answer](./Questions/E_Salary_Cities.ipynb)

**Can we determine expected salaries? 🎯**

Q6: Can we predict the salary for someone with a given years of experience and position? [answer](./Questions/P_Salary.ipynb)  </br>
Q7: What is the relationship between contract duration & salary? [answer](./Questions/E_Contract_Salary.ipynb)

**Which technology should I start with? 💻**

Q1: What is the most used technology in the mid-sized level company? [answer](./Questions/I_CompanySize_Technology.ipynb)  </br>
Q2: Can we say that the most popular technology for mid-sized companies is the most popular for big-sized companies? [answer](./Questions/I_CompanySize_Technology.ipynb)  </br>
Q4: What is the most preferred language/technology for each age segment? [answer](./Questions/D_Age_Technologies.ipynb) </br>
Q5: Is there a relation between the age of employee and the business type of the company he/she is joining? [answer](./Questions/E_Age_CompanyType.ipynb)

**Additional Questions: ❓**

Q8: How does the position (backend, frontend, etc.) affect the required years of experience needed in order to be an official senior? [answer](./Questions/E_Position_YearsOfExperience.ipynb)  </br>
Q11: What is the relation between the number of people at some seniority level with the company Type? [answer](./Questions/E_CompanyType_Seniority.ipynb)

## Project Organization 📁
The project is organized into different notebooks based on the type of question being addressed: descriptive (D), exploratory (E), inferential (I), and predictive (P). Each question has its own notebook that guides the reader through the five stages of the data science cycle, with the epicycle applied within each stage. Additionally, each question is associated with a `.py` file that contains the implementation of the utility functions used for that specific question.

## Contributors 👥
<table align="center">
  <tr>
    <td align="center">
    <a href="https://github.com/maryemsalah22" target="_black">
    <img src="https://avatars.githubusercontent.com/u/56718680?v=4" width="100px;" alt="Mariam Salah"/>
    <br />
    <sub><b>Mariam Salah</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/nadeenay" target="_black">
    <img src="https://avatars.githubusercontent.com/u/70846138?v=4" width="100px;" alt="Nadeen Ayman"/>
    <br />
    <sub><b>Nadeen Ayman</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/Halahamdy22" target="_black">
    <img src="https://avatars.githubusercontent.com/u/56937106?v=4" width="100px;" alt="Hala Hamdy"/>
    <br />
    <sub><b>Hala Hamdy</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/NouranHany" target="_black">
    <img src="https://avatars.githubusercontent.com/u/59095993?v=4" width="100px;" alt="Noran Hany"/>
    <br />
    <sub><b>Noran Hany</b></sub></a>
    </td>
  </tr>
 </table>
