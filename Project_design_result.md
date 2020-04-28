# BioCrawCraw

#### Project Description

Molecular Dynamics (MD) simulation can document the structure of the molecule(s) at atomistic resolution. Compared to genetic and static protein structure researches, there is no universal format for the input and output data as different simulation software may not be compatible to each other. 

Within the same molecule, using different simulation parameters, e.g. force field, the simulation results will be different. MD simulation results are often uploaded by individual researchers to different scientific general-purpose data repositories without integration, harmonization and validation. Therefore, generating a beautiful "look-up table" by searching and formatting the MD simulation records for a group of proteins will help to improve the interoperability and reusability of the simulation research.

This project aims to crawl Molecular Dynamic (MD) simulations available for proteins from different studies and databases with efficiency. Based on the MD filename, abstract, readme, authors and simulation parameters, we will be able to cluster or select the proteins for different purposes, e.g. COVID-19 related proteins. The automatic pipeline has the potential to outperform the conventional manual selection method.

### Git Repository

[Click here.](https://github.com/ljmesi/Copenhagen_BioHackathon2020) 

#### Code Example

For crawling, check our app on GitHub

For the keyword selection part, check the  Jupyter notebook



#### Current Progress 

- Crawl through **Figshare** for all MD files
- Pandas function to read the table and basic selection
- Multi-threads crawling performance improve

#### Current Challenges

### Team Members
- Steven Garcia

 I am a software engineer during the day and avid bioinformatics information seeker at night. I have Bachelors degree in chemistry and previously worked in several wet labs as an analytical chemist. I'm looking to better understand some of the tools used in research, and help out with Covid related topics.
- Lauri Mesilaakso

 I am almost finished with an engineering degree in molecular biotechnology with specialisation in bioinformatics (Uppsala University, Sweden). I am familiar with Python, R, AWK. Bash and Perl but the area of web scraping is very new to me. I look very much forward to be able to contribute as much as I can and learn a lot during this Biohackathon.

- Bryan White

 I have a Master degree in Biology. I did mostly molecular systematics and DNA barcoding but then moved into genomics and worked in a neurogenomics lab for a while. I am doing an MPH now to get more into health informatics.

- Jorge Hernansanz Biel

 I am a third-year bachelor bioinformatic student, currently doing his final grade project at Novo Nordisk Center for Protein Research. I am solvent with python and R , and have basic knowledge of SQL and C++ with data structures. My aim in this biohackaton is to contribute and observe the different techniques that involve web-scrapping/crawling in real scientific projects.

- Zhiwei Li

 I have a Master degree in Bioinformatics, currently working as a research assistance at the University of Copenhagen. I have done a few genetic/genomic projects using Python and R. I am looking forward to getting into the area of crawling/scraping.


### License
MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.