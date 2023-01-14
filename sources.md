
---

### Usage for teaching and learning

Here are a few examples of questions that could be posed in class, on your own, or as an assignment. Choices will depend on whether this dashboard is being used to compare ozone levels at a coastal location to those further inland, or whether the purpose is to explore the challenges and potential for working with "messy" data sets.

1. Plot just one raw data set. How much variation is there over the whole year?
2. Use zoom and scrolling functionality to estimate daily variability of this parameter.
3. What times during the year seem to have lowest ozone levels? Highest Ozone levels? How difficult is it to make these judgements
4. Plot two raw data sets. Which site appears to experience higher ozone events? At what time of year? Why might that be?
5. Are ozone variations easier to "see" by processing data with a 7-day average or by calcuating the maximum daily 8-hr average?
6. Which of these two processing options makes it easier (or more effective) to compare these two stations stations? Why?
7. Look closely at a day or two of smoothed and mda8 data. You should see they appear to be not quite "lined up". Why is this? _{{Because smoothed values are hourly wherease mda8 is a daily value assigned to the date at "0" hours. So the mda8 peak may not match up with a smoothed hourly peak. Most daily peaks are in the afternoon, especially in the summer.}}_
8. many other ideas ...

---
### Attribution

* Data used here are hourly ozone (parts per billion) for 2017 only, from 2 of many monitoring stations. Full datasets can be found at the BC Data Catalogue, [Air Quality Monitoring: Verified Hourly Data](https://catalogue.data.gov.bc.ca/dataset/77eeadf4-0c19-48bf-a47a-fa9eef01f409), licensed under the [Open Government Licence – British Columbia](https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc). 
* For more information about these data and their source, see the [Status of Ground-Level Ozone in B.C. (2015-2017)](http://www.env.gov.bc.ca/soe/indicators/air/ozone.html) web page.
* The idea is derived from a discussion between Tara Ivanochko and Rivkah Gardner-Frolick <rivkahgf@gmail.com> who uses the complete dataset as part of a [Python tutorial](https://colab.research.google.com/drive/1DO0ICvInsr74vnl3AcPBoGtJyNrV-J8F?usp=sharing#scrollTo=a5l7UD_njHPv) on importing modules, importing data, plotting timeseries and scatter plots.
* Code by [Francis Jones](https://www.eoas.ubc.ca/people/francisjones).