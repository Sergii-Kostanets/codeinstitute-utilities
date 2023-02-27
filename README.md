# **Utility Control 3**

'Utility Control 3' is an application that helps user to control your utility bills. This is the third project in the Full Stack Software Development course. And this is my third way to control my expenses. The first method of writing in a notepad is inconvenient. The second way - using mobile applications, is good, but I always dreamed of making a free system. And this third way - the program I wrote, is the first step towards fulfilling the dream of creating my application for controlling expenses.

![Utility Control 3 live](readme/images/live.png)

# Contents

* [**Project**](<#project>)
  * [Site Users Goal](<#site-users-goal>)
  * [User Stories](<#user-stories>)
  * [Site Owners Goal](<#site-owners-goal>)
* [**User Experience UX**](<#user-experience-ux>)
  * [Site Structure](<#site-structure>)
  * [Design Choices](<#design-choices>)
* [**Features**](<#features>)
  * [**Existing Features**](<#existing-features>)
    * [Header](<#header>)
    * [Buttons](<#buttons>)
    * [Main section](<#main-section>)
    * [Information section](<#information-section>)
    * [Footer](<#footer>)
  * [**Future Features**](<#future-features>)
* [**Technologies Used**](<#technologies-used>)
* [**Testing**](<#testing>)
* [**Deployment**](<#deployment>)
* [**Credits**](<#credits>)
  * [**Content**](<#content>)
  * [**Media**](<#media>)
* [**Acknowledgements**](<#acknowledgements>)

# Project

## Site Users Goal
The user of 'Utility Control 3' wants to have access to an intuitive application that saves utility bills and calculates daily usage.

## User Stories
I have included some user stories to clarify why particular feature matters. These will then be tested and confirmed in the [Testing](<#testing>) section.

- As a user, I want to be able to add expense entries.
- As a user, I want to be able to delete an expense entry in case of erroneous entries.
- As a user, I want to have access to the function to calculate the statistics of the average consumption of funds for a communal service per day.
- As a user, I want to be able to view a table with all expense records.
- As a user, I want to have an easy way to return to the main menu.

## Site Owners Goal
The goal of the site owner is to provide an application where the user can enter utility expense data in a simple way, access all expense records, view expense statistics, and delete the entry in case of incorrect input.

[Back to top](<#contents>)

# User Experience (UX)

The 'Utility Control 3' application has a command line interface with a custom theme. The color scheme is selected in such a way as to be intuitive to the user and highlight: errors, successful input, selection menu, differences in selection options, the input that must be made for this selection, menu headings.

[Back to top](<#contents>)

## Site Structure

The 'Utility Control 3' is a terminal based application that is being presented in a one page website. When the application starts the user will be presented with a short welcome message and a menu with 4 options. The menu consists of the utility choices: *electricity*, *broadband*, *food* and *gas*. Read more about the different choices in the [Features](<#features>) section.

In the top of the page there is also a 'Run Program' button that the user can use to reload the application if needed.

[Back to top](<#contents>)

## Data Model
To store all data in the application I made a choice to use [Google Sheets](https://www.google.co.uk/sheets/about/). All data in the application is being sent and retrieved from the Google Sheet.

<details><summary><b>Name of workbook: <i>codeinstitute-utility</i></b></summary>

![Google Sheet](readme/images/workbook.png)
</details><br/>

Each utility is stored on its own sheet.

<details><summary><b>Name of electricity worksheet: <i>electricity</i></b></summary>

![Google Sheet](readme/images/worksheet-electricity.png)
</details><br/>

<details><summary><b>Name of broadband worksheet: <i>broadband</i></b></summary>

![Google Sheet](readme/images/worksheet-broadband.png)
</details><br/>

<details><summary><b>Name of food worksheet: <i>food</i></b></summary>

![Google Sheet](readme/images/worksheet-food.png)
</details><br/>

<details><summary><b>Name of gas worksheet: <i>gas</i></b></summary>

![Google Sheet](readme/images/worksheet-gas.png)
</details><br/>

This structure is intended to make it easy to add other utilities in the future. Utility bills are slightly different. Electricity is calculated based on the meter readings and the price per unit of consumed energy. Gas and food bills are paid before actual consumption, so the calculation of the consumption of these indicators is carried out only after entering new data. The bill for the broadband is issued after a certain period of use of this service.

The worksheets for utilities without meter reading (*broadband*, *food* and *gas*) hold 4 columns with information such as *Date* in format *dd.mm.yyyy*, *Price* with currency *€*, *Days* quantity - *qt* and *Per day* expenses in *€*, that is being controlled from the application via Python.

The worksheet for utilitie with meter reading (*electricity*) holds 7 columns with information such as *Date* in format *dd.mm.yyyy*, *Meter* in *kWh*, *Price* with currency *€*, *Cons.* which is consumption since the last measuring in *kWh*, *Days* quantity - *qt*, *Per day* consumption in *kWh* and *Per day* expenses in *€*, that is being controlled from the application via Python.

[Back to top](<#contents>)

## Design Choices

* ### Typography
    No specific typography is being used in the application. The font is just the standard font that is being used in the terminal.

* ### Colour Scheme
    'Utility Control 3' is a terminal based application. I have used the [Rich](https://rich.readthedocs.io/en/stable/introduction.html) library for Python to be able to extend the design opportunities.

![Colour Palette image](readme/images/color-palette.png)

[Back to top](<#contents>)

# Features

When the application starts it prints the welcome message and brief description, then calls the *main* function which launches the main menu. As stated in the [Site Structure](<#site-structure>) area the application consists of 4 similar areas (different utilities): *electricity*, *broadband*, *food*, and *gas*. The features are being explained more in detail in the [Existing Features](<#existing-features>) area below.

## Existing Features

### Main Menu
The Main Menu is quite straight forward and consists of 4 choices. See each choice being explained below.

<details><summary><b>Main Menu</b></summary>

![Main Menu](readme/images/main-menu.png)
</details><br/>

[Back to top](<#contents>)

### Action Menu
The Action Menu is a submenu of Main Menu and its the same to all utilities except of the name of utility in the title. It consists of 4 different areas (functions) and an exit option: *add one row*, *delete last row*, *check statistics*, *see the table*, *go back*.

<details><summary><b>Action Menu</b></summary>

![Acrion Menu](readme/images/action-menu.png)
</details><br/>

[Back to top](<#contents>)

### Add one row
The add row to worksheet let's the user add new bill to the table. The user gets a description of the data that he is required to enter and immediately requires the first data to be entered. The required input data differs depending on the type of utility service. Date must be entered first. To help the user in the date input, the description displays the date of the previous input as well as the current date. Then the user needs to enter the meter reading, description also shows previous readings. If the utility does not provide meter readings, then this step is not displayed and is skipped. At last user needs to enter the price of utilitie, to help the user in the input, the price of the previous input is displayed.

<details><summary><b>Add one row</b></summary>

![Add one row](readme/images/add-one-row.png)
</details><br/>

[Back to top](<#contents>)

### Automatic input
For more convenient use of the program, it is possible to enter the current date and the previous price without any input data by pressing the Enter button.

<details><summary><b>Automatic input</b></summary>

![Automatic input](readme/images/automatic-input.png)
</details><br/>

[Back to top](<#contents>)

### Data validation
The previous data is shown to the user as an example of the input format. But if the input is incorrect, then the user will be shown a corresponding error and the need for input will be repeated until the user enters data in the required format.

<details><summary><b>Date validation</b></summary>

![Date validation](readme/images/validation-date.png)
</details><br/>

<details><summary><b>Meter reading validation</b></summary>

![Meter reading validation](readme/images/validation-meter-reading.png)
</details><br/>

<details><summary><b>Price validation</b></summary>

![Price validation](readme/images/validation-price.png)
</details><br/>

[Back to top](<#contents>)

### Future Features

* A registration to greet the user by name.
* A table of achievements.
* A choice of difficulty levels.
* Animation of symbol selection and win or loss process.

[Back to top](<#contents>)

## Technologies Used

* [HTML5](https://html.spec.whatwg.org/) - provides the content and structure for the website.
* [CSS3](https://www.w3.org/Style/CSS/Overview.en.html) - provides the styling.
* [JavaScript](https://www.w3schools.com/js/) - provides functionality.
* [Visual Studio Code](https://code.visualstudio.com/) - IDE used to develop the website.
* [Github](https://github.com/) - used for versin control, to deploy and host the website.
* [I Love IMG](https://www.iloveimg.com/) - online photo editor to crop and resize photos.

[Back to top](<#contents>)

## Testing

Please refer to [**_here_**](TESTING.md) for more information on testing Photo Shoot Fans.

[Back to top](<#contents>)

## Deployment

### **To deploy the project**

The site was deployed to GitHub pages. The steps to deploy a site are as follows:

  1. In the GitHub repository, navigate to the **Settings** tab.
  2. Once in Settings, navigate to the **Pages** tab on the left hand side.
  3. Under **Source**, select the branch to **main**, then click **save**.
  4. Once the main branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

![GitHub pages deployed image](assets/images/readme-images/deployment.png)

  The live link to the Github repository can be found [here](https://sergii-kostanets.github.io/codeinstitute-rock-paper-scissors-lizard-spock/).

### **To fork the repository on GitHub**

A copy of the GitHub Repository can be made by forking the GitHub account. This copy can be viewed and changes can be made to the copy without affecting the original repository. Take the following steps to fork the repository;

1. Log in to **GitHub** and locate the [repository](https://github.com/Sergii-Kostanets/codeinstitute-rock-paper-scissors-lizard-spock).
2. On the right hand side of the page inline with the repository name is a button called **'Fork'**, click on the button to create a copy of the original repository in your GitHub Account.

![GitHub forking process image](assets/images/readme-images/forking.png)

### **To create a local clone of this project**

The method from cloning a project from GitHub is below:

1. Under the repository’s name, click on the **code** tab.
2. In the **Clone with HTTPS** section, click on the clipboard icon to copy the given URL.
![Cloning image](assets/images/readme-images/clone.png)
3. In your IDE of choice, open **Git Bash**.
4. Change the current working directory to the location where you want the cloned directory to be made.
5. Type **git clone**, and then paste the URL copied from GitHub.
6. Press **enter** and the local clone will be created.

[Back to top](<#contents>)

## Credits

### Content

* The icons came from [Icon Library](https://icon-library.com/).
* Rules image came from [PNG item](https://www.pngitem.com/middle/hJJoibm_rock-paper-scissors-lizard-spock-is-a-funny/).
* Base structure, functionality and performance check came from a [Love Maths Walkthrough Project](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+LM101+2021_T1/courseware/2d651bf3f23e48aeb9b9218871912b2e/234519d86b76411aa181e76a55dabe70/).
* As an example of a readme file was taken file of author [Ewan Colquhoun](https://github.com/EwanColquhoun/wawaswoods#readme)

### Media

* The photos were compressed using [I Love IMG](https://www.iloveimg.com/).

[Back to top](<#contents>)

## Acknowledgements

The site was completed as a Portfolio 2 Project piece for the Full Stack Software Developer (e-Commerce) Diploma at the [Code Institute](https://codeinstitute.net/). As such I would like to thank my mentor [Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/), the Slack community, and all at the Code Institute for their help and support.

[Sergii Kostanets](https://sergiikostanets.netlify.app/), January 2023.

[Back to top](<#contents>)
